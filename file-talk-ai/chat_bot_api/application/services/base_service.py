"""
Base Service Class
Foundation for all service classes
"""
from abc import ABC
from chat_bot_api.core.utils.logger import get_logger


class BaseService(ABC):
    """
    Base service class that all services inherit from

    Provides common functionality like logging, error handling, etc.
    """

    def __init__(self):
        """Initialize base service"""
        self.logger = get_logger(self.__class__.__name__)

    def log_info(self, message: str, **context):
        """Log info message with context"""
        if context:
            self.logger.info(message, extra={'extra_data': context})
        else:
            self.logger.info(message)

    def log_error(self, message: str, **context):
        """Log error message with context"""
        if context:
            self.logger.error(message, extra={'extra_data': context})
        else:
            self.logger.error(message)

    def log_warning(self, message: str, **context):
        """Log warning message with context"""
        if context:
            self.logger.warning(message, extra={'extra_data': context})
        else:
            self.logger.warning(message)

    def log_debug(self, message: str, **context):
        """Log debug message with context"""
        if context:
            self.logger.debug(message, extra={'extra_data': context})
        else:
            self.logger.debug(message)
