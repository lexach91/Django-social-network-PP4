from django.test import TestCase, AsyncClient
from chats.consumers import ChatConsumer
from django.contrib.auth.models import User

class TestConsumer(TestCase):
    """Tests for the ChatConsumer class."""
    def setUp(self):
        """Set up test users"""
        pass
