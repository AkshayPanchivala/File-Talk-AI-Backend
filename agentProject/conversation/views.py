from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .question_answer_agent import questionAnswer
from .summary_agent import AnswerGenrate
from .questions_generate_agent import AgentMethods

@api_view(['POST'])
def conversationHandler(request):
    try:
        action = request.data.get('action')
        user_message = request.data.get('question')
        documentUrl = request.data.get('documenturl')

        if not action:
            return Response({"error": "Action is required."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "question_answer":
            if not user_message or not documentUrl:
                return Response({"error": "Question and Document URL are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                knowledge_base = questionAnswer.load_knowledge_base(documentUrl)
                agent = questionAnswer.initialize_agent(knowledge_base)
                answer = questionAnswer.ask_question(agent, user_message)
            except Exception as e:
                return Response({"error": f"Failed to answer question: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                "content": {  
                "success": True, 
                "data": answer
                },
                "userType": "Chatbot"
            }, status=status.HTTP_200_OK)

        elif action == "summarizer":
            if not documentUrl:
                return Response({"error": "Document URL is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                AnswerGenrate.download_pdf(documentUrl)
                text = AnswerGenrate.extract_text_from_pdf()
                answer = AnswerGenrate.summarize_text_with_agent(text)
            except Exception as e:
                return Response({"error": f"Failed to summarize document: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if not answer.get("success"):
                 return Response({"error": answer.get("error")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                "content": answer,
                "userType": "Chatbot"
            }, status=status.HTTP_200_OK)

        elif action == "generate_questions":
            if not documentUrl:
                return Response({"error": "Document URL is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                AgentMethods.download_pdf(documentUrl)
                text = AgentMethods.extract_text_from_pdf()
                answer = AgentMethods.generate_questions_and_insights(text)
            except Exception as e:
                return Response({"error": f"Failed to generate questions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if not answer.get("success"):
                 return Response({"error": answer.get("error")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                "content": answer,
                "userType": "Chatbot"
            }, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid action provided."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Unexpected server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def optionsHandler(request):
    try:
        startedChatbotId = request.data.get('startedChatbot')

        afterStartedOptions = [
            "question_answer",
            "summarizer",
            "generate_questions",
            "main_menu",
            "Exit"
        ]
        initiallyOptions = [
            "upload_document",
        ]

        if startedChatbotId:
            return Response(
                {"options": afterStartedOptions},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"options": initiallyOptions},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response({"error": f"Failed to load options: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
