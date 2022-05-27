"""Tests for the views of the friends app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from friends.models import FriendRequest
from feed.models import FriendRequestEvent

class TestViews(TestCase):
    """Tests for the views of the friends app."""

    def setUp(self):
        """Set up test users."""
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
        self.user3 = User.objects.create_user(
            username='user3',
            password='Testuser3',
            first_name='User3',
            last_name='Test',
            email='test3@test.com'
        )
        
        self.client = Client()
        self.send_friend_request_url = reverse('send-friend-request')
        self.accept_friend_request_url = reverse('accept-friend-request')
        self.decline_friend_request_url = reverse('decline-friend-request')
        self.cancel_friend_request_url = reverse('cancel-friend-request')
        self.remove_friend_url = reverse('remove-friend')
        self.my_friends_url = reverse('my-friends')
        
    def test_send_friend_request(self):
        """Test send friend request."""
        self.client.login(username='user1', password='Testuser1')
        response = self.client.post(self.send_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertJSONEqual(response.content.decode('utf-8'), {'status': 'ok'})
        self.assertEqual(FriendRequest.objects.first().from_profile, self.user1.profile)
        self.assertEqual(FriendRequest.objects.first().to_profile, self.user2.profile)
        # try to send friend request to the same user twice
        response = self.client.post(self.send_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertJSONEqual(response.content.decode('utf-8'), {'status': 'error'})
        
    def test_accept_friend_request(self):
        """Test accept friend request."""
        self.client.login(username='user1', password='Testuser1')
        # create friend request
        FriendRequest.objects.create(from_profile=self.user2.profile, to_profile=self.user1.profile)
        response = self.client.post(self.accept_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(self.user1.profile.friends.count(), 1)
        self.assertEqual(self.user2.profile.friends.count(), 1)
        self.assertEqual(self.user1.profile.friends.first(), self.user2.profile)
        self.assertEqual(self.user2.profile.friends.first(), self.user1.profile)
        
    def test_decline_friend_request(self):
        """Test decline friend request."""
        self.client.login(username='user1', password='Testuser1')
        # create friend request
        FriendRequest.objects.create(from_profile=self.user2.profile, to_profile=self.user1.profile)
        response = self.client.post(self.decline_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(self.user1.profile.friends.count(), 0)
        self.assertEqual(self.user2.profile.friends.count(), 0)
        
    def test_remove_friend(self):
        """Test remove friend."""
        self.client.login(username='user1', password='Testuser1')
        # create friend request
        FriendRequest.objects.create(from_profile=self.user2.profile, to_profile=self.user1.profile)
        self.client.post(self.accept_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(self.remove_friend_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(self.user1.profile.friends.count(), 0)
        self.assertEqual(self.user2.profile.friends.count(), 0)
        
    def test_cancel_friend_request(self):
        """Test cancel friend request."""
        self.client.login(username='user1', password='Testuser1')
        # create friend request
        FriendRequest.objects.create(from_profile=self.user1.profile, to_profile=self.user2.profile)
        FriendRequestEvent.objects.create(initiator=self.user1, target=self.user2)
        response = self.client.post(self.cancel_friend_request_url, {'profile_id': self.user2.profile.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(self.user1.profile.friends.count(), 0)
        self.assertEqual(self.user2.profile.friends.count(), 0)
        self.assertEqual(FriendRequestEvent.objects.count(), 0)
        
    def test_my_friends_view(self):
        """Test my friends view"""
        self.client.login(username='user1', password='Testuser1')
        self.user1.profile.friends.add(self.user2.profile)
        FriendRequest.objects.create(from_profile=self.user3.profile, to_profile=self.user1.profile)
        response = self.client.get(self.my_friends_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['friends'].count(), 1)
        self.assertEqual(response.context['pending_requests'].count(), 1)
        self.assertTemplateUsed(response, 'friends/my_friends.html')
