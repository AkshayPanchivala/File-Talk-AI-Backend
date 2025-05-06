from django.db import models

class Conversation(models.Model):
    chatbotId = models.CharField(max_length=255)  # fixed typo and added max_length
    content = models.CharField(max_length=1000)   # added reasonable max_length
    userType = models.CharField(max_length=50)    # user type like 'user' or 'bot'
    created_at = models.DateTimeField(auto_now_add=True)  # auto adds current time

    def __str__(self):
        return f"Conversation with {self.chatbotId} at {self.created_at}"