"""
PDF-related Exception Classes
Handles all exceptions related to PDF processing
"""
from typing import Optional, Dict, Any
from .base import BaseAppException
from config.constants import ErrorCode, HTTPStatus


class PDFException(BaseAppException):
    """Base exception for all PDF-related errors"""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.PDF_EXTRACTION_FAILED,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details
        )


class PDFDownloadError(PDFException):
    """Exception raised when PDF download fails"""

    def __init__(self, message: str = "Failed to download PDF", url: Optional[str] = None):
        details = {'url': url} if url else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.PDF_DOWNLOAD_FAILED,
            details=details
        )


class PDFInvalidFormatError(PDFException):
    """Exception raised when PDF format is invalid"""

    def __init__(self, message: str = "Invalid PDF format"):
        super().__init__(
            message=message,
            error_code=ErrorCode.PDF_INVALID_FORMAT
        )


class PDFExtractionError(PDFException):
    """Exception raised when text extraction from PDF fails"""

    def __init__(self, message: str = "Failed to extract text from PDF", page: Optional[int] = None):
        details = {'page': page} if page else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.PDF_EXTRACTION_FAILED,
            details=details
        )


class PDFTooLargeError(PDFException):
    """Exception raised when PDF file is too large"""

    def __init__(self, message: str = "PDF file is too large", max_size_mb: Optional[int] = None):
        details = {'max_size_mb': max_size_mb} if max_size_mb else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.PDF_TOO_LARGE,
            details=details
        )


class PDFURLInvalidError(PDFException):
    """Exception raised when PDF URL is invalid"""

    def __init__(self, message: str = "Invalid PDF URL", url: Optional[str] = None):
        details = {'url': url} if url else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.PDF_URL_INVALID,
            details=details
        )
