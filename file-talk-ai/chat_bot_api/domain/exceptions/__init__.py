"""Domain Exceptions"""
from .base import (
    BaseAppException,
    ValidationError,
    NotFoundError,
    InternalServerError
)
from .pdf_exceptions import (
    PDFException,
    PDFDownloadError,
    PDFInvalidFormatError,
    PDFExtractionError,
    PDFTooLargeError,
    PDFURLInvalidError
)
from .agent_exceptions import (
    AgentException,
    AgentInitializationError,
    AgentProcessingError,
    KnowledgeBaseLoadError,
    GroqAPIError,
    RateLimitExceededError,
    TimeoutError
)

__all__ = [
    # Base exceptions
    'BaseAppException',
    'ValidationError',
    'NotFoundError',
    'InternalServerError',
    # PDF exceptions
    'PDFException',
    'PDFDownloadError',
    'PDFInvalidFormatError',
    'PDFExtractionError',
    'PDFTooLargeError',
    'PDFURLInvalidError',
    # Agent exceptions
    'AgentException',
    'AgentInitializationError',
    'AgentProcessingError',
    'KnowledgeBaseLoadError',
    'GroqAPIError',
    'RateLimitExceededError',
    'TimeoutError',
]
