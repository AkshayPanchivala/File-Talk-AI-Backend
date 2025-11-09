"""
PDF Service
Handles all PDF-related operations (download, extraction, etc.)
Consolidates duplicate PDF processing code
"""
import os
import requests
import fitz  # PyMuPDF
from typing import Dict, Any, Optional
from config.env_config import config
from chat_bot_api.core.utils.helpers import FileHelper
from chat_bot_api.core.decorators.retry import retry
from chat_bot_api.domain.exceptions import (
    PDFDownloadError,
    PDFExtractionError,
    PDFInvalidFormatError,
    PDFTooLargeError
)
from .base_service import BaseService


class PDFService(BaseService):
    """Service for PDF processing operations"""

    def __init__(self):
        """Initialize PDF service"""
        super().__init__()
        self.storage_path = config.PDF_STORAGE_PATH
        self._ensure_storage_path()

    def _ensure_storage_path(self):
        """Ensure storage directory exists"""
        os.makedirs(self.storage_path, exist_ok=True)

    @retry(max_attempts=3, delay=2, exceptions=(requests.RequestException,))
    def download_pdf(self, document_url: str) -> str:
        """
        Download PDF from URL

        Args:
            document_url: URL of the PDF document

        Returns:
            str: Path to downloaded PDF file

        Raises:
            PDFDownloadError: If download fails
            PDFTooLargeError: If file is too large
        """
        self.log_info(f"Downloading PDF from {document_url}")

        try:
            response = requests.get(
                document_url,
                timeout=config.PDF_DOWNLOAD_TIMEOUT,
                stream=True
            )
            response.raise_for_status()

            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'pdf' not in content_type.lower() and not document_url.lower().endswith('.pdf'):
                raise PDFInvalidFormatError("URL does not point to a PDF file")

            # Check file size
            content_length = response.headers.get('content-length')
            if content_length:
                file_size = int(content_length)
                from config.constants import FileConstants
                if file_size > FileConstants.MAX_FILE_SIZE_BYTES:
                    raise PDFTooLargeError(
                        max_size_mb=FileConstants.MAX_FILE_SIZE_MB
                    )

            # Generate unique filename
            filename = FileHelper.generate_unique_filename(prefix='pdf_', extension='pdf')
            file_path = os.path.join(self.storage_path, filename)

            # Download file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            self.log_info(f"PDF downloaded successfully to {file_path}")
            return file_path

        except requests.exceptions.Timeout:
            self.log_error(f"Timeout downloading PDF from {document_url}")
            raise PDFDownloadError(f"Timeout downloading PDF from URL", url=document_url)

        except requests.exceptions.RequestException as e:
            self.log_error(f"Error downloading PDF: {str(e)}", error=str(e), url=document_url)
            raise PDFDownloadError(f"Failed to download PDF: {str(e)}", url=document_url)

        except IOError as e:
            self.log_error(f"File write error: {str(e)}", error=str(e))
            raise PDFDownloadError(f"Failed to save PDF file: {str(e)}")

    def extract_text_from_pdf(
        self,
        file_path: str,
        min_page: Optional[int] = None,
        max_page: Optional[int] = None
    ) -> str:
        """
        Extract text from PDF file

        Args:
            file_path: Path to PDF file
            min_page: Minimum page number (1-indexed)
            max_page: Maximum page number (1-indexed)

        Returns:
            str: Extracted text

        Raises:
            PDFExtractionError: If extraction fails
            PDFInvalidFormatError: If PDF format is invalid
        """
        self.log_info(f"Extracting text from {file_path}", min_page=min_page, max_page=max_page)

        if not os.path.exists(file_path):
            raise PDFExtractionError(f"PDF file not found: {file_path}")

        try:
            doc = fitz.open(file_path)
            total_pages = len(doc)

            # Set page range
            min_page = min_page or config.PDF_DEFAULT_MIN_PAGE
            max_page = max_page or min(config.PDF_DEFAULT_MAX_PAGE, total_pages)

            # Validate page range
            min_page = max(min_page, 1)
            max_page = min(max_page, total_pages)

            if min_page > max_page:
                raise PDFExtractionError("Minimum page cannot be greater than maximum page")

            full_text = ""

            # Extract text from each page
            for i in range(min_page - 1, max_page):
                try:
                    page = doc.load_page(i)
                    full_text += f"\n\n--- Page {i + 1} ---\n"
                    full_text += page.get_text()
                except Exception as e:
                    self.log_warning(f"Error extracting page {i + 1}: {str(e)}", page=i + 1)
                    continue

            doc.close()

            if not full_text.strip():
                raise PDFExtractionError("No text could be extracted from PDF")

            self.log_info(f"Successfully extracted text from {max_page - min_page + 1} pages")
            return full_text

        except fitz.FileDataError as e:
            self.log_error(f"Invalid PDF file: {str(e)}", error=str(e))
            raise PDFInvalidFormatError(f"Invalid PDF file format: {str(e)}")

        except Exception as e:
            self.log_error(f"Error extracting PDF text: {str(e)}", error=str(e))
            raise PDFExtractionError(f"Failed to extract text from PDF: {str(e)}")

    def cleanup_file(self, file_path: str):
        """
        Delete PDF file

        Args:
            file_path: Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.log_info(f"Cleaned up file: {file_path}")
        except Exception as e:
            self.log_warning(f"Failed to cleanup file {file_path}: {str(e)}")

    def process_pdf(
        self,
        document_url: str,
        min_page: Optional[int] = None,
        max_page: Optional[int] = None,
        cleanup: bool = True
    ) -> str:
        """
        Download and extract text from PDF (convenience method)

        Args:
            document_url: URL of the PDF
            min_page: Minimum page number
            max_page: Maximum page number
            cleanup: Whether to cleanup file after extraction

        Returns:
            str: Extracted text

        Raises:
            PDFDownloadError: If download fails
            PDFExtractionError: If extraction fails
        """
        file_path = None
        try:
            file_path = self.download_pdf(document_url)
            text = self.extract_text_from_pdf(file_path, min_page, max_page)
            return text
        finally:
            if cleanup and file_path:
                self.cleanup_file(file_path)
