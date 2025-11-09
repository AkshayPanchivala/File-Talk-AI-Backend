"""
Request Data Transfer Objects
Defines structures for API requests
"""
from dataclasses import dataclass
from typing import Optional
from chat_bot_api.domain.enums import ActionTypeEnum


@dataclass
class ConversationRequestDTO:
    """DTO for conversation request"""
    action: str
    document_url: str
    question: Optional[str] = None
    min_page: Optional[int] = None
    max_page: Optional[int] = None

    def __post_init__(self):
        """Validate and normalize data after initialization"""
        # Normalize action type
        if self.action:
            self.action = self.action.lower().strip()

        # Normalize document URL
        if self.document_url:
            self.document_url = self.document_url.strip()

    @classmethod
    def from_dict(cls, data: dict) -> 'ConversationRequestDTO':
        """
        Create DTO from dictionary

        Args:
            data: Request data dictionary

        Returns:
            ConversationRequestDTO: Request DTO instance
        """
        return cls(
            action=data.get('action', ''),
            document_url=data.get('documenturl', ''),
            question=data.get('question'),
            min_page=data.get('min_page'),
            max_page=data.get('max_page')
        )

    def validate(self) -> bool:
        """
        Validate request data

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If validation fails
        """
        from chat_bot_api.core.utils.validators import Validator

        # Validate required fields
        Validator.validate_required_fields(
            {'action': self.action, 'documenturl': self.document_url},
            ['action', 'documenturl']
        )

        # Validate action type
        Validator.validate_action_type(self.action)

        # Validate PDF URL
        Validator.validate_pdf_url(self.document_url)

        # Validate question for question_answer action
        if self.action == ActionTypeEnum.QUESTION_ANSWER.value:
            if not self.question or not self.question.strip():
                from chat_bot_api.domain.exceptions import ValidationError
                raise ValidationError("Question is required for question_answer action")

        # Validate page range if provided
        if self.min_page is not None and self.max_page is not None:
            Validator.validate_page_range(self.min_page, self.max_page)

        return True


@dataclass
class OptionsRequestDTO:
    """DTO for options request"""
    chatbot_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'OptionsRequestDTO':
        """Create DTO from dictionary"""
        return cls(
            chatbot_id=data.get('chatbotId')
        )
