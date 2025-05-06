from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Create JWT token for the user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Register a new user
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        # Validate data using the serializer
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Save user data
            user = serializer.save()

            # Generate JWT tokens
            tokens = get_tokens_for_user(user)

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            # Extract the user and tokens from the validated data
            user_data = serializer.validated_data
            tokens = user_data['tokens']

            return Response({
                "user": {
                    "id": user_data['user'].id,
                    "username": user_data['user'].username,
                    "email": user_data['user'].email,
                },
                "tokens": tokens
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
