from django.urls import path
from .views import create_chatbot

urlpatterns = [
    path('createChat/', create_chatbot, name='create_chat'),
    # path('login/', login_user, name='login_user'),
]