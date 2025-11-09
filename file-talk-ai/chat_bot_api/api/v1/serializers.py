"""
API Serializers
Django REST Framework serializers for request/response validation
"""
from rest_framework import serializers
from chat_bot_api.domain.enums import ActionTypeEnum


class ConversationRequestSerializer(serializers.Serializer):
    """Serializer for conversation requests"""

    action = serializers.ChoiceField(
        choices=ActionTypeEnum.values(),
        required=True,
        help_text="Action type to perform"
    )
    documenturl = serializers.URLField(
        required=True,
        help_text="URL of the PDF document"
    )
    question = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Question to ask (required for question_answer action)"
    )
    min_page = serializers.IntegerField(
        required=False,
        min_value=1,
        help_text="Minimum page number to process"
    )
    max_page = serializers.IntegerField(
        required=False,
        min_value=1,
        help_text="Maximum page number to process"
    )

    def validate(self, data):
        """
        Validate serializer data

        Args:
            data: Validated data dictionary

        Returns:
            dict: Validated data

        Raises:
            serializers.ValidationError: If validation fails
        """
        action = data.get('action')
        question = data.get('question')

        # Validate question for question_answer action
        if action == ActionTypeEnum.QUESTION_ANSWER.value:
            if not question or not question.strip():
                raise serializers.ValidationError({
                    'question': 'Question is required for question_answer action'
                })

        # Validate page range
        min_page = data.get('min_page')
        max_page = data.get('max_page')

        if min_page and max_page:
            if min_page > max_page:
                raise serializers.ValidationError({
                    'max_page': 'Maximum page must be greater than or equal to minimum page'
                })

        # Validate PDF URL
        documenturl = data.get('documenturl', '')
        if not documenturl.lower().endswith('.pdf'):
            raise serializers.ValidationError({
                'documenturl': 'URL must point to a PDF file'
            })

        return data


class OptionsRequestSerializer(serializers.Serializer):
    """Serializer for options requests"""

    chatbotId = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Chatbot ID (optional)"
    )
    startedChatbot = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether chatbot has been started (default: True)"
    )


class ConversationResponseSerializer(serializers.Serializer):
    """Serializer for conversation responses"""

    content = serializers.DictField(
        help_text="Response content"
    )
    userType = serializers.CharField(
        default='Chatbot',
        help_text="Type of user (User or Chatbot)"
    )


class OptionsResponseSerializer(serializers.Serializer):
    """Serializer for options responses"""

    options = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of available options"
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""

    error = serializers.DictField(
        help_text="Error details"
    )
