"""Tests for the views of the profiles app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profile


class TestViews(TestCase):
    """Tests for the views of the profiles app."""

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
        self.client = Client()
        self.my_profile_url = reverse('my_profile')
        self.edit_avatar_url = reverse('edit_avatar_ajax')
        self.edit_profile_url = reverse('edit_profile')
        self.reset_avatar_url = reverse('reset-avatar')
        self.delete_user_url = reverse('delete-user')
        self.check_online_url = reverse('check_online')
        self.user_profile_url = reverse(
            'user_profile', kwargs={'username': self.user2.username})

    def test_my_profile_view(self):
        """Test my_profile view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_profile.html')
        self.assertEqual(response.context['user_profile'], self.user.profile)
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('post_form', response.context)
        self.assertIn('comment_form', response.context)
        self.assertIn('posts', response.context)
        self.assertIn('edit_profile_form', response.context)
        self.assertIn('edit_avatar_form', response.context)

    def test_user_profile_view(self):
        """Test user_profile view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/user_profile.html')
        self.assertEqual(response.context['user_profile'], self.user2.profile)
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('post_form', response.context)
        self.assertIn('comment_form', response.context)
        self.assertIn('posts', response.context)

    def test_edit_avatar_view(self):
        """Test edit_avatar view."""
        self.client.login(username='user', password='Testuser1')
        avatar = open('static/images/phone.png', 'rb')
        response = self.client.post(
            self.edit_avatar_url,
            {'avatar': avatar},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_edit_profile_view(self):
        """Test edit_profile view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('profile_form', response.context)
        self.assertIn('avatar_form', response.context)
        self.assertIn('password_form', response.context)

    def test_reset_avatar_view(self):
        """Test reset_avatar view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.post(
            self.reset_avatar_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_check_online_view(self):
        """Test check_online view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.get(
            self.check_online_url,
            {'username': self.user2.username},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['online'], False)
        response = self.client.get(
            self.check_online_url,
            {'username': self.user.username},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['online'], True)

    def test_delete_user_view(self):
        """Test delete_user view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.post(
            self.delete_user_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='user').count(), 0)
