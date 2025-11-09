"""
AI Agent-related Exception Classes
Handles all exceptions related to AI agent operations
"""
from typing import Optional, Dict, Any
from .base import BaseAppException
from config.constants import ErrorCode, HTTPStatus


class AgentException(BaseAppException):
    """Base exception for all AI agent-related errors"""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.AGENT_PROCESSING_FAILED,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=details
        )


class AgentInitializationError(AgentException):
    """Exception raised when agent initialization fails"""

    def __init__(self, message: str = "Failed to initialize AI agent", agent_name: Optional[str] = None):
        details = {'agent_name': agent_name} if agent_name else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.AGENT_INITIALIZATION_FAILED,
            details=details
        )


class AgentProcessingError(AgentException):
    """Exception raised when agent processing fails"""

    def __init__(self, message: str = "AI agent processing failed", agent_name: Optional[str] = None):
        details = {'agent_name': agent_name} if agent_name else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.AGENT_PROCESSING_FAILED,
            details=details
        )


class KnowledgeBaseLoadError(AgentException):
    """Exception raised when knowledge base loading fails"""

    def __init__(self, message: str = "Failed to load knowledge base", source: Optional[str] = None):
        details = {'source': source} if source else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.KNOWLEDGE_BASE_LOAD_FAILED,
            details=details
        )


class GroqAPIError(AgentException):
    """Exception raised when Groq API calls fail"""

    def __init__(self, message: str = "Groq API error occurred", api_response: Optional[str] = None):
        details = {'api_response': api_response} if api_response else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.GROQ_API_ERROR,
            details=details
        )


class RateLimitExceededError(AgentException):
    """Exception raised when API rate limit is exceeded"""

    def __init__(self, message: str = "API rate limit exceeded", retry_after: Optional[int] = None):
        details = {'retry_after_seconds': retry_after} if retry_after else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            status_code=429,  # Too Many Requests
            details=details
        )


class TimeoutError(AgentException):
    """Exception raised when operation times out"""

    def __init__(self, message: str = "Operation timed out", timeout_seconds: Optional[int] = None):
        details = {'timeout_seconds': timeout_seconds} if timeout_seconds else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.TIMEOUT_ERROR,
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            details=details
        )
