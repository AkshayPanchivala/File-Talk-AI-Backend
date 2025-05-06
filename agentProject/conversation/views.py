import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .question_answer_agent import questionAnswer
from .summary_agent import AnswerGenrate
from .questions_generate_agent import AgentMethods

# @api_view(['POST'])
@api_view(['POST'])
def conversationHandler(request):
    action=request.data.get('action')
    user_message = request.data.get('question')
    documentUrl = request.data.get('documenturl')
    # agent_type=request.data.get('agent_type')
    if action=="question_answer":
        if not user_message or not documentUrl :
            return Response({"error": "Message and Document are required."}, status=status.HTTP_400_BAD_REQUEST)

        knowledge_base = questionAnswer.load_knowledge_base(documentUrl)
        agent = questionAnswer.initialize_agent(knowledge_base)
        answer=questionAnswer.ask_question(agent, user_message)    

    
        return Response({
            # "chatbotId": chatbotId,
            "content": answer,
            "userType": "Chatbot"
        }, status=status.HTTP_200_OK)
    elif action=="summarizer":
        if not documentUrl :
            return Response({"error": "Message and Document are required."}, status=status.HTTP_400_BAD_REQUEST)
        knowledge_base=  AnswerGenrate.download_pdf(documentUrl)
        text = AnswerGenrate.extract_text_from_pdf()
        answer=AnswerGenrate.summarize_text_with_agent(text)
        # knowledge_base = questionAnswer.load_knowledge_base(documentUrl)
        # agent = questionAnswer.initialize_agent(knowledge_base)
        # answer=questionAnswer.ask_question(agent, user_message)    
  
    
        return Response({
            # "chatbotId": chatbotId,
            "content": answer,
            "userType": "Chatbot"
        }, status=status.HTTP_200_OK)
    elif action=="generate_questions":
        if  not documentUrl :
            return Response({"error": "Message and Document are required."}, status=status.HTTP_400_BAD_REQUEST)

        knowledge_base = AgentMethods.download_pdf(documentUrl)
        text = AgentMethods.extract_text_from_pdf()
        answer=AgentMethods.generate_questions_and_insights(text)  

    
        return Response({
            # "chatbotId": chatbotId,
            "content": answer,
            "userType": "Chatbot"
        }, status=status.HTTP_200_OK)
    
    
    
    



@api_view(['POST'])
def optionsHandler(request):
    startedChatbotId = request.data.get('startedChatbot')
    afterStatedoptions=[
        "question_answer",
        "summarizer",
        "generate_questions",
        "main_menu",
        "Exit"
    ]
    initallyOptions=[
        "upload_document",
    ]
    if startedChatbotId:
        return Response(
            {
                "options": afterStatedoptions,
            }, 
            status=status.HTTP_200_OK)
    else:
        return Response(
            {
                "options": initallyOptions,
            }, 
            status=status.HTTP_200_OK)
    
    