"""
Logging Utility
Provides structured logging for the application
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from config.env_config import config


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add custom fields if present
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data)


class Logger:
    """
    Application logger with structured logging support

    Usage:
        logger = Logger.get_logger(__name__)
        logger.info("User logged in", extra_data={'user_id': 123})
    """

    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger instance

        Args:
            name: Logger name (typically __name__)

        Returns:
            logging.Logger: Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, config.LOG_LEVEL))

        # Remove existing handlers
        logger.handlers = []

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)

        # Set formatter based on config
        if config.LOG_FORMAT == 'json':
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Prevent propagation to root logger
        logger.propagate = False

        cls._loggers[name] = logger
        return logger

    @staticmethod
    def log_with_context(
        logger: logging.Logger,
        level: str,
        message: str,
        **context: Any
    ):
        """
        Log message with additional context

        Args:
            logger: Logger instance
            level: Log level (INFO, ERROR, etc.)
            message: Log message
            **context: Additional context data
        """
        log_method = getattr(logger, level.lower())
        extra = {'extra_data': context} if context else {}
        log_method(message, extra=extra)


# Convenience function
def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger
    """
    return Logger.get_logger(name)
