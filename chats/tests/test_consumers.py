"""Tests for the consumers of the chats app."""
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from channels.sessions import SessionMiddlewareStack
from chats.consumers import ChatConsumer
from chats.models import Chat, Message
from django.contrib.auth.models import User
from django.test import TestCase, override_settings, Client
from asgiref.sync import sync_to_async
import json


class AuthWebsocketCommunicator(WebsocketCommunicator):
    """Websocket communicator that authenticates users."""

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.scope['user'] = user
            self.scope['url_route'] = {'kwargs': {'room_name': user.username}}

class TestChatConsumer(TestCase):
    """Tests for the consumers of the chats app."""
    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='user1',
            password='Testuser1',
            first_name='User1',
            last_name='Test',
            email='test1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testuser2',
            first_name='User2',
            last_name='Test',
            email='test2@test.com'
        )
        
        self.app = ChatConsumer()
        self.channel_layer = get_channel_layer()
        self.client = Client()
        
    async def test_connect(self):
        """Test connecting to the websocket"""
        # await sync_to_async(self.client.login)(username='user1', password='Testuser1')
        communicator = AuthWebsocketCommunicator(
            user=self.user1,
            application=self.app,
            path='/ws/chat-with-user2/',
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.assertEqual(communicator.scope['user'], self.user1)
        self.assertEqual(communicator.scope['url_route']['kwargs']['room_name'], self.user1.username)
        await communicator.disconnect()
