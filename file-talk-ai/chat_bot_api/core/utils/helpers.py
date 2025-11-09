"""
Helper Utilities
Provides common helper functions
"""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


class FileHelper:
    """File-related helper functions"""

    @staticmethod
    def generate_unique_filename(prefix: str = '', extension: str = '') -> str:
        """
        Generate unique filename

        Args:
            prefix: Filename prefix
            extension: File extension (with or without dot)

        Returns:
            str: Unique filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]

        # Ensure extension starts with dot
        if extension and not extension.startswith('.'):
            extension = f'.{extension}'

        return f"{prefix}{timestamp}_{unique_id}{extension}"

    @staticmethod
    def get_file_hash(content: bytes, algorithm: str = 'md5') -> str:
        """
        Generate hash of file content

        Args:
            content: File content as bytes
            algorithm: Hash algorithm (md5, sha256, etc.)

        Returns:
            str: File hash
        """
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(content)
        return hash_func.hexdigest()

    @staticmethod
    def get_url_hash(url: str) -> str:
        """
        Generate hash of URL

        Args:
            url: URL string

        Returns:
            str: URL hash
        """
        return hashlib.md5(url.encode()).hexdigest()


class ResponseHelper:
    """API response helper functions"""

    @staticmethod
    def success_response(
        data: Any,
        message: str = "Success",
        status_code: int = 200
    ) -> Dict[str, Any]:
        """
        Create success response

        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code

        Returns:
            dict: Success response dictionary
        """
        return {
            'success': True,
            'message': message,
            'data': data,
            'status_code': status_code
        }

    @staticmethod
    def error_response(
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ) -> Dict[str, Any]:
        """
        Create error response

        Args:
            message: Error message
            error_code: Application error code
            details: Additional error details
            status_code: HTTP status code

        Returns:
            dict: Error response dictionary
        """
        response = {
            'success': False,
            'error': {
                'code': error_code,
                'message': message,
            },
            'status_code': status_code
        }

        if details:
            response['error']['details'] = details

        return response


class StringHelper:
    """String manipulation helper functions"""

    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = '...') -> str:
        """
        Truncate text to specified length

        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add to truncated text

        Returns:
            str: Truncated text
        """
        if len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Convert text to snake_case

        Args:
            text: Text to convert

        Returns:
            str: Snake case text
        """
        # Replace non-alphanumeric with underscore
        text = re.sub(r'[^a-zA-Z0-9]+', '_', text)
        # Convert to lowercase
        return text.lower().strip('_')

    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        Convert text to camelCase

        Args:
            text: Text to convert

        Returns:
            str: Camel case text
        """
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


import re


class DateTimeHelper:
    """DateTime helper functions"""

    @staticmethod
    def get_current_timestamp() -> str:
        """Get current ISO format timestamp"""
        return datetime.utcnow().isoformat()

    @staticmethod
    def format_timestamp(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Format datetime to string

        Args:
            dt: Datetime object
            format_str: Format string

        Returns:
            str: Formatted datetime string
        """
        return dt.strftime(format_str)
