"""
Application Constants
Centralized location for all application constants
"""
from enum import Enum


# API Configuration
class APIVersion:
    """API Version Constants"""
    V1 = 'v1'
    CURRENT = V1


# HTTP Status Codes
class HTTPStatus:
    """HTTP Status Code Constants"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


# Error Codes
class ErrorCode:
    """Application Error Codes"""
    # General Errors
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'
    NOT_FOUND = 'NOT_FOUND'

    # PDF Errors
    PDF_DOWNLOAD_FAILED = 'PDF_DOWNLOAD_FAILED'
    PDF_INVALID_FORMAT = 'PDF_INVALID_FORMAT'
    PDF_EXTRACTION_FAILED = 'PDF_EXTRACTION_FAILED'
    PDF_TOO_LARGE = 'PDF_TOO_LARGE'
    PDF_URL_INVALID = 'PDF_URL_INVALID'

    # Agent Errors
    AGENT_INITIALIZATION_FAILED = 'AGENT_INITIALIZATION_FAILED'
    AGENT_PROCESSING_FAILED = 'AGENT_PROCESSING_FAILED'
    KNOWLEDGE_BASE_LOAD_FAILED = 'KNOWLEDGE_BASE_LOAD_FAILED'

    # API Errors
    GROQ_API_ERROR = 'GROQ_API_ERROR'
    RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'
    TIMEOUT_ERROR = 'TIMEOUT_ERROR'


# Action Types
class ActionType:
    """Conversation Action Types"""
    QUESTION_ANSWER = 'question_answer'
    SUMMARIZER = 'summarizer'
    GENERATE_QUESTIONS = 'generate_questions'

    @classmethod
    def get_all(cls) -> list:
        """Get all action types"""
        return [cls.QUESTION_ANSWER, cls.SUMMARIZER, cls.GENERATE_QUESTIONS]

    @classmethod
    def is_valid(cls, action: str) -> bool:
        """Check if action type is valid"""
        return action in cls.get_all()


# User Types
class UserType:
    """User Type Constants"""
    USER = 'User'
    CHATBOT = 'Chatbot'
    SYSTEM = 'System'


# File Constants
class FileConstants:
    """File-related Constants"""
    ALLOWED_EXTENSIONS = ['pdf']
    MAX_FILE_SIZE_MB = 50
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    # Temporary file naming
    TEMP_FILE_PREFIX = 'temp_'
    PDF_FILE_EXTENSION = '.pdf'


# Agent Configuration
class AgentConstants:
    """AI Agent Configuration Constants"""
    # Default prompts
    QA_FALLBACK_MESSAGE = "I'm sorry, but I couldn't find the answer to your question in the provided PDF document."

    # Agent names
    QA_AGENT_NAME = "PDF-Only QA Agent"
    SUMMARY_AGENT_NAME = "Summarizer"
    QUESTION_GEN_AGENT_NAME = "QuestionGenerator"

    # Agent roles
    QA_AGENT_ROLE = "Answer user questions using only the content of a specific PDF file."
    SUMMARY_AGENT_ROLE = "PDF summarizer"
    QUESTION_GEN_AGENT_ROLE = "PDF educational assistant"


# Cache Keys
class CacheKey:
    """Cache Key Prefixes"""
    PDF_CONTENT = 'pdf_content'
    KNOWLEDGE_BASE = 'knowledge_base'
    SUMMARY = 'summary'
    QUESTIONS = 'questions'

    @staticmethod
    def pdf_content_key(url: str) -> str:
        """Generate cache key for PDF content"""
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{CacheKey.PDF_CONTENT}:{url_hash}"

    @staticmethod
    def knowledge_base_key(url: str) -> str:
        """Generate cache key for knowledge base"""
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{CacheKey.KNOWLEDGE_BASE}:{url_hash}"


# Regex Patterns
class RegexPatterns:
    """Common Regular Expression Patterns"""
    URL_PATTERN = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
    PDF_URL_PATTERN = r'^https?://.*\.pdf$'
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


# Time Constants
class TimeConstants:
    """Time-related Constants"""
    # In seconds
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    ONE_HOUR = 3600
    ONE_DAY = 86400

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    RETRY_BACKOFF_MULTIPLIER = 2


# Logging Constants
class LoggingConstants:
    """Logging Configuration Constants"""
    # Log levels
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    # Log message templates
    REQUEST_STARTED = "Request started: {method} {path}"
    REQUEST_COMPLETED = "Request completed: {method} {path} - Status: {status} - Duration: {duration}ms"
    ERROR_OCCURRED = "Error occurred: {error_type} - {message}"


# Response Messages
class ResponseMessage:
    """Standard Response Messages"""
    # Success messages
    SUCCESS = "Operation completed successfully"
    PDF_DOWNLOADED = "PDF downloaded successfully"
    PDF_PROCESSED = "PDF processed successfully"

    # Error messages
    INVALID_REQUEST = "Invalid request data"
    MISSING_REQUIRED_FIELD = "Missing required field: {field}"
    INVALID_ACTION = "Invalid action type. Allowed values: {allowed_actions}"
    PDF_DOWNLOAD_FAILED = "Failed to download PDF from the provided URL"
    PDF_PROCESSING_FAILED = "Failed to process PDF document"
    AGENT_ERROR = "An error occurred while processing your request"
    INTERNAL_ERROR = "An internal error occurred. Please try again later"

    # Validation messages
    INVALID_URL = "Invalid URL format"
    INVALID_PDF_URL = "URL does not point to a PDF file"
    INVALID_PAGE_RANGE = "Invalid page range specified"


# Database Constants
class DatabaseConstants:
    """Database-related Constants"""
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


# Security Constants
class SecurityConstants:
    """Security-related Constants"""
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = 60
    RATE_LIMIT_PER_HOUR = 1000

    # API Key rotation
    API_KEY_ROTATION_DAYS = 90
