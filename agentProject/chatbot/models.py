from django.db import models


# Create your models here.
class ChatBot(models.Model):
    name=models.CharField(max_length=100, unique=True)
    userid=models.CharField()
    discription=models.CharField()
    document=models.CharField()

    def __str__(self):
        return self.username

