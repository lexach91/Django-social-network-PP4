"""Tests for the views of the chats app."""
from django.test import TestCase, Client
from django.urls import reverse
from chats.models import Chat, Message
from django.contrib.auth.models import User


class TestViews(TestCase):
    """Tests for the views of the chats app."""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='user1',
            password='Testuser1',
            first_name='User1',
            last_name='Test',
            email='testuser@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testuser2',
            first_name='User2',
            last_name='Test',
            email='testuser2@example.com'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            password='Testuser3',
            first_name='User3',
            last_name='Test',
            email='testuser3@example.com'
        )

        self.client = Client()
        self.my_messages_url = reverse('my_messages')
        self.get_message_time_url = reverse('get_message_time')
        self.update_message_read_status_url = reverse(
            'update_message_read_status')

    def test_my_messages_view(self):
        """Test my messages view"""
        self.client.login(username='user1', password='Testuser1')
        response = self.client.get(self.my_messages_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/my_messages.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['chats'].count(), 0)
        chat1 = Chat.objects.create()
        chat1.members.add(self.user1, self.user2)
        response = self.client.get(self.my_messages_url)
        self.assertEqual(response.context['chats'].count(), 1)
        chat2 = Chat.objects.create()
        chat2.members.add(self.user1, self.user3)
        response = self.client.get(self.my_messages_url)
        self.assertEqual(response.context['chats'].count(), 2)

    def test_chat_view(self):
        """Test chat view"""
        self.client.login(username='user1', password='Testuser1')
        self.user1.profile.friends.add(self.user2.profile)
        chat_detail_url = reverse('chat_detail', kwargs={
                                  'username': self.user2.username})
        response = self.client.get(chat_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chats/chat_detail.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(response.context['chat'].members.count(), 2)
        self.assertEqual(response.context['chat'].members.first(), self.user1)
        self.assertEqual(response.context['chat'].members.last(), self.user2)
        self.assertEqual(response.context['chat'].messages.count(), 0)
        self.assertEqual(response.context['second_user'], self.user2)
        chat_id = response.context['chat'].id
        self.assertEqual(response.context['room_name'], chat_id)
        message1 = Message.objects.create(
            chat=response.context['chat'],
            author=self.user1,
            content='Test message'
        )
        response = self.client.get(chat_detail_url)
        self.assertEqual(response.context['chat'].messages.count(), 1)
        self.assertEqual(response.context['chat'].messages.first(), message1)
        self.assertEqual(
            response.context['chat'].messages.first().author, self.user1)
        self.assertEqual(
            response.context['chat'].messages.first().content, 'Test message')

    def test_get_message_time_view(self):
        """Test get message time ajax view"""
        self.client.login(username='user1', password='Testuser1')
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat,
            author=self.user1,
            content='Test message'
        )
        message_id = message.id
        response = self.client.post(
            self.get_message_time_url,
            {'message_id': message_id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(
            'utf-8'), {'sent_at': message.sent_at})

    def test_update_message_read_status(self):
        """Test update message is_read status ajax view"""
        self.client.login(username='user1', password='Testuser1')
        chat = Chat.objects.create()
        chat.members.add(self.user1, self.user2)
        message = Message.objects.create(
            chat=chat,
            author=self.user1,
            content='Test message'
        )
        self.assertEqual(message.is_read, False)
        message_id = message.id
        self.client.post(
            self.update_message_read_status_url,
            {'message_id': message_id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(Message.objects.get(id=message_id).is_read, True)
