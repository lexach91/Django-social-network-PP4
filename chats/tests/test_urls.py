"""Tests for the urls of the chats app."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chats.views import (
    MyMessagesView,
    ChatView,
    GetMessageTimeView,
    UpdateMessageReadStatusView
)


class TestUrls(SimpleTestCase):
    """Tests for the urls of the chats app."""

    def test_my_messages_url(self):
        """Test my messages url"""
        url = reverse('my_messages')
        self.assertEqual(resolve(url).func.view_class, MyMessagesView)

    def test_chat_url(self):
        """Test chat url"""
        url = reverse('chat_detail', args=['user2'])
        self.assertEqual(resolve(url).func.view_class, ChatView)

    def test_get_message_time_url(self):
        """Test get message time url"""
        url = reverse('get_message_time')
        self.assertEqual(resolve(url).func.view_class, GetMessageTimeView)

    def test_update_message_read_status_url(self):
        """Test update message read status url"""
        url = reverse('update_message_read_status')
        self.assertEqual(resolve(url).func.view_class,
                         UpdateMessageReadStatusView)
