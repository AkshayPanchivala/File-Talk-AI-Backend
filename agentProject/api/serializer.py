from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration (with password hashing).
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Include password field here

    def create(self, validated_data):
        # Hash password before saving
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # create_user automatically hashes password
        user.set_password(password)
        user.save()
        return user

    # Field-level validation for email
    def validate_email(self, value):
        if "@example.com" in value:
            raise serializers.ValidationError("Registration with @example.com emails is not allowed.")
        return value

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login (authenticate the user and generate JWT token).
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the username and password and return user if authenticated.
        """
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
