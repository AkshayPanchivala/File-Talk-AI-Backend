"""
Validation Utilities
Provides validation functions for common data types
"""
import re
from typing import Optional
from urllib.parse import urlparse
from config.constants import RegexPatterns, FileConstants
from chat_bot_api.domain.exceptions import ValidationError


class Validator:
    """Utility class for data validation"""

    @staticmethod
    def validate_url(url: str, require_https: bool = False) -> bool:
        """
        Validate URL format

        Args:
            url: URL to validate
            require_https: Require HTTPS protocol

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If URL is invalid
        """
        if not url or not isinstance(url, str):
            raise ValidationError("URL must be a non-empty string")

        # Check URL format
        if not re.match(RegexPatterns.URL_PATTERN, url):
            raise ValidationError(f"Invalid URL format: {url}")

        # Parse URL
        parsed = urlparse(url)

        # Check for HTTPS if required
        if require_https and parsed.scheme != 'https':
            raise ValidationError("URL must use HTTPS protocol")

        return True

    @staticmethod
    def validate_pdf_url(url: str) -> bool:
        """
        Validate PDF URL

        Args:
            url: PDF URL to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If URL is invalid or doesn't point to PDF
        """
        # First validate as regular URL
        Validator.validate_url(url)

        # Check if URL ends with .pdf (basic check)
        if not url.lower().endswith('.pdf'):
            raise ValidationError(
                f"URL does not point to a PDF file: {url}",
                details={'url': url}
            )

        return True

    @staticmethod
    def validate_page_range(
        min_page: int,
        max_page: int,
        total_pages: Optional[int] = None
    ) -> bool:
        """
        Validate page range

        Args:
            min_page: Minimum page number
            max_page: Maximum page number
            total_pages: Total pages in document (optional)

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If page range is invalid
        """
        if min_page < 1:
            raise ValidationError("Minimum page must be greater than 0")

        if max_page < min_page:
            raise ValidationError(
                "Maximum page must be greater than or equal to minimum page"
            )

        if total_pages and max_page > total_pages:
            raise ValidationError(
                f"Maximum page ({max_page}) exceeds total pages ({total_pages})"
            )

        return True

    @staticmethod
    def validate_required_fields(data: dict, required_fields: list) -> bool:
        """
        Validate required fields in dictionary

        Args:
            data: Data dictionary
            required_fields: List of required field names

        Returns:
            bool: True if all fields present

        Raises:
            ValidationError: If required field is missing
        """
        missing_fields = [
            field for field in required_fields
            if field not in data or data[field] is None or data[field] == ''
        ]

        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}",
                details={'missing_fields': missing_fields}
            )

        return True

    @staticmethod
    def validate_action_type(action: str) -> bool:
        """
        Validate action type

        Args:
            action: Action type string

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If action type is invalid
        """
        from chat_bot_api.domain.enums import ActionTypeEnum

        if not ActionTypeEnum.is_valid(action):
            raise ValidationError(
                f"Invalid action type: {action}",
                details={
                    'provided': action,
                    'allowed_values': ActionTypeEnum.values()
                }
            )

        return True

    @staticmethod
    def validate_file_size(size_bytes: int, max_size_bytes: Optional[int] = None) -> bool:
        """
        Validate file size

        Args:
            size_bytes: File size in bytes
            max_size_bytes: Maximum allowed size in bytes

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If file is too large
        """
        max_size = max_size_bytes or FileConstants.MAX_FILE_SIZE_BYTES

        if size_bytes > max_size:
            max_size_mb = max_size / (1024 * 1024)
            actual_size_mb = size_bytes / (1024 * 1024)
            raise ValidationError(
                f"File size ({actual_size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb:.2f}MB)",
                details={
                    'file_size_mb': actual_size_mb,
                    'max_size_mb': max_size_mb
                }
            )

        return True

    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input

        Args:
            text: Text to sanitize
            max_length: Maximum length (optional)

        Returns:
            str: Sanitized text
        """
        if not isinstance(text, str):
            return str(text)

        # Remove null bytes
        sanitized = text.replace('\x00', '')

        # Trim whitespace
        sanitized = sanitized.strip()

        # Truncate if needed
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized
