from django.urls import path
from .views import conversationHandler,optionsHandler
urlpatterns = [
    path("/conversation/",conversationHandler,name="chat_bot_message"),
    path("/options/",optionsHandler,name="chat_bot_options")
]
