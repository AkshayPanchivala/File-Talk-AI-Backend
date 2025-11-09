"""
API Validators
Additional validation functions for API requests
"""
from rest_framework import serializers
from chat_bot_api.core.utils.validators import Validator
from chat_bot_api.domain.exceptions import ValidationError as DomainValidationError


def validate_conversation_request(data: dict) -> dict:
    """
    Validate conversation request data

    Args:
        data: Request data

    Returns:
        dict: Validated data

    Raises:
        serializers.ValidationError: If validation fails
    """
    try:
        # Validate PDF URL
        document_url = data.get('documenturl', '')
        Validator.validate_pdf_url(document_url)

        # Validate action type
        action = data.get('action', '')
        Validator.validate_action_type(action)

        # Validate page range if provided
        min_page = data.get('min_page')
        max_page = data.get('max_page')

        if min_page is not None and max_page is not None:
            Validator.validate_page_range(min_page, max_page)

        return data

    except DomainValidationError as e:
        raise serializers.ValidationError(str(e))
