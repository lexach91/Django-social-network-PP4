from django.urls import path
from .views import MyMessagesView


urlpatterns = [
    path('', MyMessagesView.as_view(), name='my_messages'),
]