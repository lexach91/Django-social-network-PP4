from django.urls import re_path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r'ws/chat-with-<str:username>', ChatConsumer.as_asgi()),
    re_path(r'wss/chat-with-<str:username>/', ChatConsumer.as_asgi()),
]
