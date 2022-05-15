from django.urls import path
from .views import MyMessagesView, ChatView, GetMessageTimeView


urlpatterns = [
    path('', MyMessagesView.as_view(), name='my_messages'),
    path('chat-with-<str:username>/', ChatView.as_view(), name='chat_detail'),
    path('get-message-time/', GetMessageTimeView.as_view(), name='get_message_time'),
]