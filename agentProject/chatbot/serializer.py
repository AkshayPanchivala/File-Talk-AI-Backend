from rest_framework import serializers
from .models import ChatBot
from rest_framework.exceptions import ValidationError

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = ['id', 'name', 'discription','document', 'userid']  # Include relevant fields

    def create(self, validated_data):
        name = serializers.CharField()
        discription= serializers.CharField()
        document=serializers.CharField()
        userid=serializers.CharField()

        """
        Custom create method to add logic during ChatBot creation.
        The user ID will be extracted from the JWT token in the request.
        """

        
        # Create and return the ChatBot instance
        return ChatBot.objects.create(**validated_data)
