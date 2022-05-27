"""Tests for the url patterns of the home app."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import HomeView


class TestUrls(SimpleTestCase):
    """Test the urls for the home app."""

    def test_home_url_resolves(self):
        """Test the home url"""
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)
