"""Tests for the views of the communities app."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from communities.views import (
    UsersCommunitiesView,
    CommunityView,
    JoinCommunityView,
    LeaveCommunityView,
    CreateCommunityView,
    EditCommunityView,
    DeleteCommunityView,
)


class TestUrls(SimpleTestCase):
    """Test the urls for the communities app"""

    def test_users_communities_url_resolves(self):
        url = reverse('users_communities')
        self.assertEquals(resolve(url).func.view_class, UsersCommunitiesView)

    def test_community_url_resolves(self):
        url = reverse('community', args=['test-community'])
        self.assertEquals(resolve(url).func.view_class, CommunityView)

    def test_join_community_url_resolves(self):
        url = reverse('join_community', args=['test-community'])
        self.assertEquals(resolve(url).func.view_class, JoinCommunityView)

    def test_leave_community_url_resolves(self):
        url = reverse('leave_community', args=['test-community'])
        self.assertEquals(resolve(url).func.view_class, LeaveCommunityView)

    def test_create_community_url_resolves(self):
        url = reverse('create_community')
        self.assertEquals(resolve(url).func.view_class, CreateCommunityView)

    def test_edit_community_url_resolves(self):
        url = reverse('edit_community', args=['test-community'])
        self.assertEquals(resolve(url).func.view_class, EditCommunityView)

    def test_delete_community_url_resolves(self):
        url = reverse('delete_community', args=['test-community'])
        self.assertEquals(resolve(url).func.view_class, DeleteCommunityView)
