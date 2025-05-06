from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import ChatBotSerializer

@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Automatically reject unauthenticated requests
def create_chatbot(request):
    """
    Create a new ChatBot instance. The authenticated user ID is automatically assigned.
    """
    # Ensure the request has an authenticated user
    print("sssssssssssssssssssssssss")
    print("Headers: ", request.headers)
    # if not request.user.is_authenticated:
    #     return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    print(request) 
    # Pass the `request` context to the serializer to access the authenticated user in the serializer
    serializer = ChatBotSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the serializer; user ID will be automatically set inside the serializer
        chatbot = serializer.save()
        # print(chatbot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
