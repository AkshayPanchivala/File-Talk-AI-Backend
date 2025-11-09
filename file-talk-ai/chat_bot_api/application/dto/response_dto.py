"""
Response Data Transfer Objects
Defines structures for API responses
"""
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List
from chat_bot_api.domain.enums import UserTypeEnum


@dataclass
class ConversationResponseDTO:
    """DTO for conversation response"""
    content: Dict[str, Any]
    user_type: str = UserTypeEnum.CHATBOT.value

    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return asdict(self)

    @classmethod
    def success(cls, data: Any, message: str = "Success") -> 'ConversationResponseDTO':
        """
        Create success response

        Args:
            data: Response data
            message: Success message

        Returns:
            ConversationResponseDTO: Success response DTO
        """
        return cls(
            content={
                'success': True,
                'message': message,
                'data': data
            },
            user_type=UserTypeEnum.CHATBOT.value
        )

    @classmethod
    def error(cls, message: str, error_code: str, details: Optional[Dict[str, Any]] = None) -> 'ConversationResponseDTO':
        """
        Create error response

        Args:
            message: Error message
            error_code: Application error code
            details: Additional error details

        Returns:
            ConversationResponseDTO: Error response DTO
        """
        content = {
            'success': False,
            'error': {
                'code': error_code,
                'message': message
            }
        }

        if details:
            content['error']['details'] = details

        return cls(
            content=content,
            user_type=UserTypeEnum.CHATBOT.value
        )


@dataclass
class OptionsResponseDTO:
    """DTO for options response"""
    options: List[Dict[str, str]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return {'options': self.options}

    @classmethod
    def default_options(cls) -> 'OptionsResponseDTO':
        """
        Get default chat options (when chatbot is started)

        Returns:
            OptionsResponseDTO: Default options response
        """
        from chat_bot_api.domain.enums import ActionTypeEnum

        options = [
            {
                'action': ActionTypeEnum.QUESTION_ANSWER.value,
                'label': 'Ask a Question',
                'description': 'Get answers from your PDF document'
            },
            {
                'action': ActionTypeEnum.SUMMARIZER.value,
                'label': 'Summarize Document',
                'description': 'Get a comprehensive summary of your PDF'
            },
            {
                'action': ActionTypeEnum.GENERATE_QUESTIONS.value,
                'label': 'Generate Questions',
                'description': 'Generate study questions from your PDF'
            },
            {
                'action': 'main_menu',
                'label': 'Main Menu',
                'description': 'Go back to main menu and start a new conversation'
            }
        ]

        return cls(options=options)

    @classmethod
    def upload_only_options(cls) -> 'OptionsResponseDTO':
        """
        Get upload-only option (when chatbot hasn't started)

        Returns:
            OptionsResponseDTO: Upload-only option response
        """
        options = [
            {
                'action': 'upload_file',
                'label': 'Upload PDF File',
                'description': 'Upload a PDF document to start chatting'
            }
        ]

        return cls(options=options)


@dataclass
class ErrorResponseDTO:
    """DTO for error responses"""
    error: Dict[str, Any]
    status_code: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return {'error': self.error}

    @classmethod
    def from_exception(cls, exception) -> 'ErrorResponseDTO':
        """
        Create error response from exception

        Args:
            exception: Exception instance

        Returns:
            ErrorResponseDTO: Error response DTO
        """
        from chat_bot_api.domain.exceptions import BaseAppException

        if isinstance(exception, BaseAppException):
            return cls(
                error={
                    'code': exception.error_code,
                    'message': exception.message,
                    'details': exception.details
                },
                status_code=exception.status_code
            )
        else:
            # Handle unexpected exceptions
            from config.constants import ErrorCode, HTTPStatus
            return cls(
                error={
                    'code': ErrorCode.INTERNAL_ERROR,
                    'message': str(exception),
                    'details': {}
                },
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
