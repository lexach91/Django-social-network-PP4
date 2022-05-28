"""Tests for the views of the search app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from communities.models import Community


class TestViews(TestCase):
    """Tests for the views of the search app."""

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
        self.community = Community.objects.create(
            name="Test Community",
            description="Test Description",
            creator=self.user
        )
        self.client = Client()
        self.search_url = reverse('search')
        self.search_people_url = reverse('search_people_ajax')
        self.search_communities_url = reverse('search_communities_ajax')

    def test_search_view(self):
        """Test search view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertIn('profiles', response.context)
        self.assertIn('communities', response.context)

    def test_search_people_view(self):
        """Test search_people view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.post(
            self.search_people_url,
            {'search_query': 'user2'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'profiles': [
                    {
                        'username': self.user2.username,
                        'name': str(self.user2.profile),
                        'avatar': self.user2.profile.avatar_url,
                        'online': self.user2.profile.online
                    }
                ]
            }
        )

    def test_search_communities_view(self):
        """Test search_communities view."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.post(
            self.search_communities_url,
            {'search_query': 'community'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'communities': [
                    {
                        'name': self.community.name,
                        'description': self.community.description,
                        'logo': self.community.logo_url,
                        'slug': self.community.slug,
                        'member_count': self.community.member_count
                    }
                ]
            }
        )
