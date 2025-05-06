from django.urls import path
from .views import conversationHandler,optionsHandler
urlpatterns = [
    path("/",conversationHandler,name="conversation_chat"),
    path("/options/",optionsHandler,name="conversation_chat_options")
]
