"""
Environment Configuration Management
Handles loading and validating environment variables
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path


class EnvironmentConfig:
    """Central configuration class for environment variables"""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize configuration by loading environment variables"""
        if self._initialized:
            return

        # Load .env file from project root
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)

        # Load and validate required environment variables
        self._load_variables()
        self._initialized = True

    def _load_variables(self):
        """Load all environment variables"""
        # API Keys
        self.GROQ_API_KEY: str = self._get_required('groqApiKey')

        # AI Model Configuration
        self.GROQ_MODEL_ID: str = os.getenv('GROQ_MODEL_ID', 'llama-3.3-70b-versatile')
        self.AI_TEMPERATURE: float = float(os.getenv('AI_TEMPERATURE', '0.7'))
        self.AI_MAX_TOKENS: int = int(os.getenv('AI_MAX_TOKENS', '8000'))

        # PDF Processing Configuration
        self.PDF_DOWNLOAD_TIMEOUT: int = int(os.getenv('PDF_DOWNLOAD_TIMEOUT', '30'))
        self.PDF_MAX_PAGES: int = int(os.getenv('PDF_MAX_PAGES', '100'))
        self.PDF_DEFAULT_MIN_PAGE: int = int(os.getenv('PDF_DEFAULT_MIN_PAGE', '1'))
        self.PDF_DEFAULT_MAX_PAGE: int = int(os.getenv('PDF_DEFAULT_MAX_PAGE', '5'))
        self.PDF_STORAGE_PATH: str = os.getenv('PDF_STORAGE_PATH', 'media/pdfs')

        # Summary Configuration
        self.SUMMARY_MIN_WORDS: int = int(os.getenv('SUMMARY_MIN_WORDS', '8000'))

        # Question Generation Configuration
        self.QUESTIONS_COUNT: int = int(os.getenv('QUESTIONS_COUNT', '20'))

        # Cache Configuration
        self.CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'False').lower() == 'true'
        self.CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
        self.REDIS_URL: Optional[str] = os.getenv('REDIS_URL')

        # Storage Configuration
        self.STORAGE_BACKEND: str = os.getenv('STORAGE_BACKEND', 'local')  # 'local' or 's3'
        self.AWS_ACCESS_KEY_ID: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.AWS_STORAGE_BUCKET_NAME: Optional[str] = os.getenv('AWS_STORAGE_BUCKET_NAME')
        self.AWS_S3_REGION_NAME: Optional[str] = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')

        # Logging Configuration
        self.LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')  # 'json' or 'text'

        # Feature Flags
        self.ENABLE_RATE_LIMITING: bool = os.getenv('ENABLE_RATE_LIMITING', 'False').lower() == 'true'
        self.ENABLE_MONITORING: bool = os.getenv('ENABLE_MONITORING', 'False').lower() == 'true'

        # Environment
        self.ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
        self.DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'

    def _get_required(self, key: str) -> str:
        """
        Get required environment variable

        Args:
            key: Environment variable key

        Returns:
            str: Environment variable value

        Raises:
            ValueError: If required environment variable is not set
        """
        value = os.getenv(key)
        if value is None or value == '':
            raise ValueError(
                f"Required environment variable '{key}' is not set. "
                f"Please check your .env file."
            )
        return value

    def get(self, key: str, default=None):
        """
        Get configuration value by key

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return getattr(self, key, default)

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == 'production'

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == 'development'

    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.ENVIRONMENT.lower() == 'testing'


# Global configuration instance
config = EnvironmentConfig()
