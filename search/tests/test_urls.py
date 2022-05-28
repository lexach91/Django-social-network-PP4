"""Tests for the urls of the search app"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from search.views import SearchView, SearchPeopleAjax, SearchCommunitiesAjax


class TestUrls(SimpleTestCase):
    """Test the urls for the search app"""

    def test_search_url_resolves(self):
        """Test the search url"""
        url = reverse('search')
        self.assertEquals(resolve(url).func.view_class, SearchView)

    def test_search_people_ajax_url_resolves(self):
        """Test the search people ajax url"""
        url = reverse('search_people_ajax')
        self.assertEquals(resolve(url).func.view_class, SearchPeopleAjax)

    def test_search_communities_ajax_url_resolves(self):
        """Test the search communities ajax url"""
        url = reverse('search_communities_ajax')
        self.assertEquals(resolve(url).func.view_class, SearchCommunitiesAjax)
