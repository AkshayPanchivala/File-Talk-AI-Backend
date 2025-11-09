"""
Retry Decorator
Provides retry functionality for operations that may fail transiently
"""
import time
import functools
from typing import Callable, Type, Tuple
from chat_bot_api.core.utils.logger import get_logger

logger = get_logger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry a function on failure

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each attempt
        exceptions: Tuple of exception types to catch

    Usage:
        @retry(max_attempts=3, delay=2, backoff=2)
        def unstable_operation():
            # Code that may fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay

            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts",
                            extra={'extra_data': {
                                'function': func.__name__,
                                'attempts': attempt,
                                'error': str(e)
                            }}
                        )
                        raise

                    logger.warning(
                        f"Function {func.__name__} failed on attempt {attempt}/{max_attempts}. "
                        f"Retrying in {current_delay}s...",
                        extra={'extra_data': {
                            'function': func.__name__,
                            'attempt': attempt,
                            'max_attempts': max_attempts,
                            'delay': current_delay,
                            'error': str(e)
                        }}
                    )

                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1

        return wrapper
    return decorator
