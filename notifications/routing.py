from django.urls import re_path
from .consumers import NotificationConsumer


websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
    re_path(r'wss/notifications/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
]
