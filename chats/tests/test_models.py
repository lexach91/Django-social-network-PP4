"""Tests for the models of the chats app."""
from django.test import TestCase
from django.contrib.auth.models import User
from chats.models import Chat, Message
import datetime


class TestModels(TestCase):
    """Test models of the chats app"""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username="user1",
            password="Testuser1",
            first_name="User1",
            last_name="Test",
            email="testuser@example.com",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Testuser2",
            first_name="User2",
            last_name="Test",
            email="testuser2@example.com",
        )

    def test_chat_creation(self):
        """Test chat creation"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        self.assertEqual(chat.members.count(), 2)
        self.assertEqual(chat.members.first(), self.user1)
        self.assertEqual(chat.members.last(), self.user2)

    def test_message_creation(self):
        """Test message creation"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        self.assertEqual(message.chat, chat)
        self.assertEqual(message.author, self.user1)
        self.assertEqual(message.content, "Test message")

    def test_chat_unread_messages_count(self):
        """Test unread messages count"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        # self.assertEqual(chat.unread_messages_count(), 0)
        message.is_read = True
        message.save()
        self.assertEqual(chat.unread_messages_count(), 0)
        message.is_read = False
        message.save()
        self.assertEqual(chat.unread_messages_count(), 1)

    def test_chat_last_message_at(self):
        """Test last message at"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        # compare time without microseconds
        self.assertEqual(
            chat.last_message_at.replace(microsecond=0),
            message.created_at.replace(microsecond=0),
        )

    def test_chat_str(self):
        """Test chat string representation"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        self.assertEqual(
            str(chat),
            "Chat between {}".format(
                " and ".join(
                    [member.username for member in chat.members.all()])
            ),
        )

    def test_message_str(self):
        """Test message string representation"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        self.assertEqual(str(message), str(
            message.content).replace("<br>", " "))

    def test_chat_get_last_message(self):
        """Test get last message"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        self.assertEqual(chat.get_last_message(), message)

    def test_chat_get_last_message_none(self):
        """Test get last message none"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        self.assertEqual(chat.get_last_message(), None)

    def test_message_sent_at(self):
        """Test message sent at"""
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat, author=self.user1, content="Test message"
        )
        self.assertEqual(message.sent_at, "just now")
        message.created_at = message.created_at - datetime.timedelta(seconds=2)
        self.assertEqual(message.sent_at, "a few seconds ago")
        message.created_at = message.created_at - datetime.timedelta(seconds=8)
        self.assertEqual(message.sent_at, "10 seconds ago")
        message.created_at = message.created_at - datetime.timedelta(minutes=1)
        self.assertEqual(message.sent_at, "a minute ago")
        message.created_at = message.created_at - datetime.timedelta(minutes=2)
        self.assertEqual(message.sent_at, "3 minutes ago")
        message.created_at = message.created_at - \
            datetime.timedelta(minutes=60)
        self.assertEqual(message.sent_at, "an hour ago")
        message.created_at = message.created_at - \
            datetime.timedelta(minutes=120)
        self.assertEqual(message.sent_at, "3 hours ago")
        message.created_at = message.created_at - datetime.timedelta(hours=24)
        self.assertEqual(message.sent_at, "Yesterday")
        message.created_at = message.created_at - datetime.timedelta(days=6)
        self.assertEqual(message.sent_at, "7 days ago")
        message.created_at = message.created_at - datetime.timedelta(days=30)
        self.assertEqual(message.sent_at, "a month ago")
        message.created_at = message.created_at - datetime.timedelta(days=60)
        self.assertEqual(message.sent_at, "3 months ago")
        message.created_at = message.created_at - datetime.timedelta(days=365)
        self.assertEqual(message.sent_at, "a year ago")
        message.created_at = message.created_at - \
            datetime.timedelta(days=365 * 2)
        self.assertEqual(message.sent_at, "3 years ago")
