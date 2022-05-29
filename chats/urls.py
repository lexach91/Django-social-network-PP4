from django.urls import path
from .views import (
    MyMessagesView,
    ChatView,
    GetMessageTimeView,
    UpdateMessageReadStatusView
)


urlpatterns = [
    path('', MyMessagesView.as_view(), name='my_messages'),
    path('chat-with-<str:username>/', ChatView.as_view(), name='chat_detail'),
    path(
        'get-message-time/',
        GetMessageTimeView.as_view(),
        name='get_message_time'
    ),
    path(
        'update-message-read-status/',
        UpdateMessageReadStatusView.as_view(),
        name='update_message_read_status'
    ),
]
