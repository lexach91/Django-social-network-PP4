"""Tests for the urls of the posts app"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts.views import (
    CreatePostAjaxView,
    LikePostAjaxView,
    DislikePostAjaxView,
    CreateCommentAjaxView,
    LikeCommentAjaxView,
    DislikeCommentAjaxView,
    EditPostAjaxView,
    EditCommentAjaxView,
    DeletePostAjaxView,
    DeleteCommentAjaxView
)


class TestUrls(SimpleTestCase):
    """Test the urls for the posts app"""

    def test_create_post_ajax_url_resolves(self):
        """Test the create post ajax url"""
        url = reverse('create_post_ajax')
        self.assertEquals(resolve(url).func.view_class, CreatePostAjaxView)

    def test_like_post_ajax_url_resolves(self):
        """Test the like post ajax url"""
        url = reverse('like_post_ajax')
        self.assertEquals(resolve(url).func.view_class, LikePostAjaxView)

    def test_dislike_post_ajax_url_resolves(self):
        """Test the dislike post ajax url"""
        url = reverse('dislike_post_ajax')
        self.assertEquals(resolve(url).func.view_class, DislikePostAjaxView)

    def test_create_comment_ajax_url_resolves(self):
        """Test the create comment ajax url"""
        url = reverse('create_comment_ajax')
        self.assertEquals(resolve(url).func.view_class, CreateCommentAjaxView)

    def test_like_comment_ajax_url_resolves(self):
        """Test the like comment ajax url"""
        url = reverse('like_comment_ajax')
        self.assertEquals(resolve(url).func.view_class, LikeCommentAjaxView)

    def test_dislike_comment_ajax_url_resolves(self):
        """Test the dislike comment ajax url"""
        url = reverse('dislike_comment_ajax')
        self.assertEquals(resolve(url).func.view_class, DislikeCommentAjaxView)

    def test_edit_post_ajax_url_resolves(self):
        """Test the edit post ajax url"""
        url = reverse('edit_post_ajax')
        self.assertEquals(resolve(url).func.view_class, EditPostAjaxView)

    def test_edit_comment_ajax_url_resolves(self):
        """Test the edit comment ajax url"""
        url = reverse('edit_comment_ajax')
        self.assertEquals(resolve(url).func.view_class, EditCommentAjaxView)

    def test_delete_post_ajax_url_resolves(self):
        """Test the delete post ajax url"""
        url = reverse('delete_post_ajax')
        self.assertEquals(resolve(url).func.view_class, DeletePostAjaxView)

    def test_delete_comment_ajax_url_resolves(self):
        """Test the delete comment ajax url"""
        url = reverse('delete_comment_ajax')
        self.assertEquals(resolve(url).func.view_class, DeleteCommentAjaxView)
