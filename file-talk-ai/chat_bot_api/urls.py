from django.urls import path
from .api.v1.views import conversation_handler, options_handler

urlpatterns = [
    path("conversation/", conversation_handler, name="chat_bot_message"),
    path("options/", options_handler, name="chat_bot_options")
]
