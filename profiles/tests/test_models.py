"""Tests for the models of the profiles app."""
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from friends.models import FriendRequest
import cloudinary
import cloudinary.uploader
from datetime import date


class TestModels(TestCase):
    """Tests for the models of the profiles app."""

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username="user",
            password="Testuser1",
            first_name="User",
            last_name="Test",
            email="test@test.com"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Testuser2",
            first_name="User2",
            last_name="Test2",
            email="test2@test.com"
        )
        
    def test_profile_creation(self):
        """Test profile creation."""
        # profile should already exist because of signals
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(Profile.objects.get(user=self.user).user, self.user)
        self.assertEqual(Profile.objects.get(user=self.user2).user, self.user2)
        
    def test_profile_update(self):
        """Test profile update."""
        # profile should already exist because of signals
        profile = Profile.objects.get(user=self.user)
        profile.avatar = cloudinary.uploader.upload_image("static/images/default_avatar.svg")
        profile.bio = "Test bio"
        profile.birth_date = "2000-01-01"
        profile.save()
        self.assertTrue('res.cloudinary.com' in profile.avatar.url)
        self.assertEqual(profile.bio, "Test bio")
        self.assertEqual(profile.birth_date, "2000-01-01")
        self.assertEqual(Profile.objects.count(), 2)
        
    def test_profile_str(self):
        """Test profile string representation."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), "user")
        profile.first_name = "User"
        profile.last_name = "Test"
        self.assertEqual(str(profile), "User Test")
        
    def test_profile_avatar_url(self):
        """Test profile avatar_url property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.avatar_url, "/static/images/default_avatar.svg")
        profile.avatar = cloudinary.uploader.upload_image("static/images/default_avatar.svg")
        profile.save()
        self.assertTrue('res.cloudinary.com' in profile.avatar_url)
        
    def test_profile_location(self):
        """Test profile location property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.location, None)
        profile.country = "Test country"
        self.assertEqual(profile.location, "Test country")
        profile.country = None
        profile.city = "Test city"
        self.assertEqual(profile.location, "Test city")
        profile.country = "Test country"
        self.assertEqual(profile.location, "Test country, Test city")
        
    def test_profile_age(self):
        """Test profile age property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.age, None)
        profile.birth_date = date(1990, 1, 1)
        self.assertEqual(profile.age, 32)
        profile.birth_date = date(1999, 1, 1)
        self.assertEqual(profile.age, 23)
        profile.birth_date = date(2000, 1, 1)
        self.assertEqual(profile.age, 22)
        
    def test_profile_pending_friends_in(self):
        """Test profile pending_friends_in property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.pending_friends_in, [])
        friend_request = FriendRequest.objects.create(
            from_profile=self.user2.profile,
            to_profile=profile
        )
        self.assertEqual(profile.pending_friends_in, [self.user2.profile])
        
    def test_profile_pending_requests_count(self):
        """Test profile pending_requests_count property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.pending_requests_count, 0)
        friend_request = FriendRequest.objects.create(
            from_profile=self.user2.profile,
            to_profile=profile
        )
        self.assertEqual(profile.pending_requests_count, 1)
