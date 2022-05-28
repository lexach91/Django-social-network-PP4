"""Tests for the views of the home app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestHomeViews(TestCase):
    """Test the views of the home app."""

    def setUp(self):
        """Create a user for the tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='Testuser1',
            first_name='User',
            last_name='Test',
            email='test@test.com'
        )
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_url_unauthorized_user(self):
        """Test the home url."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_url_authorized_user(self):
        """Test the home url."""
        self.client.login(username='testuser', password='Testuser1')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('feed'))
