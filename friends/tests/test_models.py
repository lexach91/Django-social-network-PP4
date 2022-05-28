"""Tests for the models of the friends app."""
from django.test import TestCase
from django.contrib.auth.models import User
from friends.models import FriendRequest


class TestModels(TestCase):
    """Tests for the models of the friends app."""

    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(
            username="user1",
            password="Testuser1",
            first_name="User1",
            last_name="Test",
            email="test1@test.com"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Testuser2",
            first_name="User2",
            last_name="Test",
            email="test2@test.com"
        )

    def test_friend_request_creation(self):
        """Test friend request creation."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        self.assertEqual(friend_request.from_profile, self.user1.profile)
        self.assertEqual(friend_request.to_profile, self.user2.profile)
        self.assertEqual(friend_request.accepted, False)
        self.assertEqual(friend_request.declined, False)

    def test_friend_request_accept(self):
        """Test friend request accept."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        friend_request.accept()
        self.assertEqual(friend_request.accepted, True)
        self.assertEqual(friend_request.declined, False)

    def test_friend_request_decline(self):
        """Test friend request decline."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        friend_request.decline()
        self.assertEqual(friend_request.accepted, False)
        self.assertEqual(friend_request.declined, True)

    def test_friend_request_is_accepted(self):
        """Test friend request is accepted."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        friend_request.accept()
        self.assertEqual(friend_request.is_accepted(), True)

    def test_friend_request_is_declined(self):
        """Test friend request is declined."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        friend_request.decline()
        self.assertEqual(friend_request.is_declined(), True)

    def test_friend_request_is_pending(self):
        """Test friend request is pending."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        self.assertEqual(friend_request.is_pending(), True)

    def test_friend_request_get_all_requests(self):
        """Test friend request get all requests."""
        friend_request1 = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        self.assertEqual(FriendRequest.get_all_requests().count(), 1)
        friend_request2 = FriendRequest.objects.create(
            from_profile=self.user2.profile,
            to_profile=self.user1.profile,
        )
        self.assertEqual(FriendRequest.get_all_requests().count(), 2)

    def test_friend_request_get_pending_requests(self):
        """Test friend request get pending requests."""
        friend_request1 = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        self.assertEqual(FriendRequest.get_pending_requests().count(), 1)
        friend_request2 = FriendRequest.objects.create(
            from_profile=self.user2.profile,
            to_profile=self.user1.profile,
        )
        self.assertEqual(FriendRequest.get_pending_requests().count(), 2)
        friend_request1.accept()
        self.assertEqual(FriendRequest.get_pending_requests().count(), 1)
        friend_request2.decline()
        self.assertEqual(FriendRequest.get_pending_requests().count(), 0)

    def test_friend_request_str(self):
        """Test friend request str."""
        friend_request = FriendRequest.objects.create(
            from_profile=self.user1.profile,
            to_profile=self.user2.profile,
        )
        self.assertEqual(str(friend_request), "user1 to user2")
        friend_request2 = FriendRequest.objects.create(
            from_profile=self.user2.profile,
            to_profile=self.user1.profile,
        )
        self.assertEqual(str(friend_request2), "user2 to user1")
