"""
API Views (v1)
Refactored views using enterprise architecture
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from chat_bot_api.core.utils.logger import get_logger
from chat_bot_api.domain.enums import ActionTypeEnum
from chat_bot_api.domain.exceptions import BaseAppException
from chat_bot_api.application.dto import (
    ConversationRequestDTO,
    ConversationResponseDTO,
    OptionsResponseDTO,
    ErrorResponseDTO
)
from chat_bot_api.application.services import (
    QuestionAnswerService,
    SummaryService,
    QuestionGenerationService
)
from .serializers import (
    ConversationRequestSerializer,
    OptionsRequestSerializer
)

logger = get_logger(__name__)


@api_view(['GET', 'POST'])
def conversation_handler(request):
    """
    Handle conversation requests

    Endpoints:
        GET: Returns API information
        POST: Process conversation (question answering, summarization, question generation)

    Args:
        request: HTTP request

    Returns:
        Response: HTTP response
    """
    if request.method == 'GET':
        return Response({
            'message': 'File Talk AI - Conversation API',
            'version': 'v1',
            'endpoints': {
                'POST /conversation/': 'Process conversation',
                'POST /options/': 'Get available options'
            }
        })

    # POST request handling
    try:
        logger.info(f"Received conversation request", extra={'extra_data': {
            'method': request.method,
            'data': request.data
        }})

        # Validate request data using serializer
        serializer = ConversationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid request data", extra={'extra_data': {
                'errors': serializer.errors
            }})
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create DTO from validated data
        request_dto = ConversationRequestDTO.from_dict(serializer.validated_data)

        # Validate DTO
        request_dto.validate()

        # Process based on action type
        action = request_dto.action

        if action == ActionTypeEnum.QUESTION_ANSWER.value:
            response_dto = _handle_question_answer(request_dto)

        elif action == ActionTypeEnum.SUMMARIZER.value:
            response_dto = _handle_summarization(request_dto)

        elif action == ActionTypeEnum.GENERATE_QUESTIONS.value:
            response_dto = _handle_question_generation(request_dto)

        else:
            # This should never happen due to serializer validation
            return Response(
                {'error': f'Invalid action: {action}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Request processed successfully", extra={'extra_data': {
            'action': action
        }})

        return Response(response_dto.to_dict(), status=status.HTTP_200_OK)

    except BaseAppException as e:
        # Handle application exceptions
        logger.error(f"Application error: {str(e)}", extra={'extra_data': {
            'error_code': e.error_code,
            'error': str(e)
        }})

        error_dto = ErrorResponseDTO.from_exception(e)
        return Response(
            error_dto.to_dict(),
            status=error_dto.status_code
        )

    except Exception as e:
        # Handle unexpected exceptions
        logger.error(f"Unexpected error: {str(e)}", extra={'extra_data': {
            'error': str(e)
        }}, exc_info=True)

        from config.constants import ErrorCode, HTTPStatus
        error_dto = ErrorResponseDTO(
            error={
                'code': ErrorCode.INTERNAL_ERROR,
                'message': 'An internal error occurred',
                'details': {'error': str(e)} if logger.level == 10 else {}  # Include details in DEBUG mode
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

        return Response(
            error_dto.to_dict(),
            status=error_dto.status_code
        )


@api_view(['POST'])
def options_handler(request):
    """
    Handle options requests

    Returns available conversation options based on chatbot state

    Args:
        request: HTTP request

    Returns:
        Response: HTTP response with available options
    """
    try:
        logger.info("Received options request", extra={'extra_data': {
            'payload': request.data
        }})

        # Validate request
        serializer = OptionsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get startedChatbot state from request
        started_chatbot = request.data.get('startedChatbot', True)

        # Return options based on state
        if started_chatbot:
            # Chatbot already started - return all conversation options
            response_dto = OptionsResponseDTO.default_options()
        else:
            # Chatbot not started - return only file upload option
            response_dto = OptionsResponseDTO.upload_only_options()

        logger.info("Options request processed successfully", extra={'extra_data': {
            'started_chatbot': started_chatbot,
            'options_count': len(response_dto.options)
        }})

        return Response(response_dto.to_dict(), status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error processing options request: {str(e)}", exc_info=True)

        return Response(
            {'error': 'Failed to retrieve options'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Helper functions for handling specific actions

def _handle_question_answer(request_dto: ConversationRequestDTO) -> ConversationResponseDTO:
    """
    Handle question answering action

    Args:
        request_dto: Request DTO

    Returns:
        ConversationResponseDTO: Response DTO
    """
    logger.info("Processing question answer request")

    service = QuestionAnswerService()
    answer = service.answer_question(
        document_url=request_dto.document_url,
        question=request_dto.question
    )

    return ConversationResponseDTO.success(
        data=answer,
        message="Question answered successfully"
    )


def _handle_summarization(request_dto: ConversationRequestDTO) -> ConversationResponseDTO:
    """
    Handle document summarization action

    Args:
        request_dto: Request DTO

    Returns:
        ConversationResponseDTO: Response DTO
    """
    logger.info("Processing document summarization request")

    service = SummaryService()
    summary = service.summarize_document(
        document_url=request_dto.document_url,
        min_page=request_dto.min_page,
        max_page=request_dto.max_page
    )

    return ConversationResponseDTO.success(
        data=summary,
        message="Document summarized successfully"
    )


def _handle_question_generation(request_dto: ConversationRequestDTO) -> ConversationResponseDTO:
    """
    Handle question generation action

    Args:
        request_dto: Request DTO

    Returns:
        ConversationResponseDTO: Response DTO
    """
    logger.info("Processing question generation request")

    service = QuestionGenerationService()
    questions = service.generate_questions(
        document_url=request_dto.document_url,
        min_page=request_dto.min_page,
        max_page=request_dto.max_page
    )

    return ConversationResponseDTO.success(
        data=questions,
        message="Questions generated successfully"
    )
