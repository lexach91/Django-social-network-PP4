from django.urls import path
from .views import MyMessagesView, ChatView


urlpatterns = [
    path('', MyMessagesView.as_view(), name='my_messages'),
    path('chat-with-<str:username>/', ChatView.as_view(), name='chat_detail'),
]