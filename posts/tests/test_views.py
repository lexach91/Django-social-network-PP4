"""Tests for the views of the posts app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Comment, POST_TYPE_CHOICES


class TestViews(TestCase):
    """Tests for the views of the posts app."""

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username="user",
            password="Testuser1",
            first_name="User",
            last_name="Test",
            email="test@test.com"
        )
        self.client = Client()
        self.create_post_url = reverse('create_post_ajax')
        self.like_post_url = reverse('like_post_ajax')
        self.dislike_post_url = reverse('dislike_post_ajax')
        self.create_comment_url = reverse('create_comment_ajax')
        self.like_comment_url = reverse('like_comment_ajax')
        self.dislike_comment_url = reverse('dislike_comment_ajax')
        self.edit_post_url = reverse('edit_post_ajax')
        self.delete_post_url = reverse('delete_post_ajax')
        self.edit_comment_url = reverse('edit_comment_ajax')
        self.delete_comment_url = reverse('delete_comment_ajax')
        
    def test_create_post_ajax(self):
        """Test create post ajax."""
        self.client.login(username='user', password='Testuser1')
        response = self.client.post(self.create_post_url, {
            'content': 'Test post',
            'post_type': POST_TYPE_CHOICES[0][0]
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
        self.assertEqual(Post.objects.first().content, 'Test post')
        self.assertEqual(Post.objects.first().post_type, POST_TYPE_CHOICES[0][0])
        
    def test_like_post_ajax(self):
        """Test like post ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        response = self.client.post(self.like_post_url, {
            'post_id': post.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().get_likes(), 1)
        
    def test_dislike_post_ajax(self):
        """Test dislike post ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        response = self.client.post(self.dislike_post_url, {
            'post_id': post.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().get_dislikes(), 1)
        
    def test_create_comment_ajax(self):
        """Test create comment ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        response = self.client.post(self.create_comment_url, {
            'post_id': post.id,
            'comment_content': 'Test comment'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)
        self.assertEqual(Comment.objects.first().content, 'Test comment')
        self.assertEqual(Comment.objects.first().post, post)
        
    def test_like_comment_ajax(self):
        """Test like comment ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            author=self.user,
            content="Test comment",
            post=post
        )
        response = self.client.post(self.like_comment_url, {
            'comment_id': comment.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.first().get_likes(), 1)
        
    def test_dislike_comment_ajax(self):
        """Test dislike comment ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            author=self.user,
            content="Test comment",
            post=post
        )
        response = self.client.post(self.dislike_comment_url, {
            'comment_id': comment.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.first().get_dislikes(), 1)
        
    def test_edit_post_ajax(self):
        """Test edit post ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        response = self.client.post(self.edit_post_url, {
            'post_id': post.id,
            'content': 'Test post edited',
            'post_type': POST_TYPE_CHOICES[0][0]
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().content, 'Test post edited')
        
    def test_delete_post_ajax(self):
        """Test delete post ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        response = self.client.post(self.delete_post_url, {
            'post_id': post.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_edit_comment_ajax(self):
        """Test edit comment ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            author=self.user,
            content="Test comment",
            post=post
        )
        response = self.client.post(self.edit_comment_url, {
            'comment_id': comment.id,
            'comment_content': 'Test comment edited'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.first().content, 'Test comment edited')
        
    def test_delete_comment_ajax(self):
        """Test delete comment ajax."""
        self.client.login(username='user', password='Testuser1')
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            author=self.user,
            content="Test comment",
            post=post
        )
        response = self.client.post(self.delete_comment_url, {
            'comment_id': comment.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
