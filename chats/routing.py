from django.urls import re_path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r'^my_messages/chat-with-(?P<username>[\w.@+-]+)/$', ChatConsumer.as_asgi()),
]
