"""Tests for the url patterns of the feed app."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from feed.views import FeedView


class TestUrls(SimpleTestCase):
    """Test the urls for the feed app."""

    def test_feed_url_resolves(self):
        """Test the feed url"""
        url = reverse('feed')
        self.assertEquals(resolve(url).func.view_class, FeedView)
