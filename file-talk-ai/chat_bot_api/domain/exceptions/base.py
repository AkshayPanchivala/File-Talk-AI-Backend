"""
Base Exception Classes
Foundation for all custom exceptions in the application
"""
from typing import Optional, Dict, Any
from config.constants import ErrorCode, HTTPStatus


class BaseAppException(Exception):
    """
    Base exception class for all application exceptions

    Attributes:
        message: Human-readable error message
        error_code: Application-specific error code
        status_code: HTTP status code
        details: Additional error details
    """

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.INTERNAL_ERROR,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format for API responses"""
        error_dict = {
            'error': {
                'code': self.error_code,
                'message': self.message,
            }
        }

        if self.details:
            error_dict['error']['details'] = self.details

        return error_dict

    def __str__(self):
        return f"{self.error_code}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message}, error_code={self.error_code})"


class ValidationError(BaseAppException):
    """Exception raised for validation errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details
        )


class NotFoundError(BaseAppException):
    """Exception raised when a resource is not found"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND,
            details=details
        )


class InternalServerError(BaseAppException):
    """Exception raised for internal server errors"""

    def __init__(self, message: str = "An internal error occurred", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=details
        )
