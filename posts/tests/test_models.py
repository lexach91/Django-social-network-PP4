"""Tests for the models of the posts app."""
from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post, Comment, POST_TYPE_CHOICES
import cloudinary
import cloudinary.uploader



class TestModels(TestCase):
    """Tests for the models of the posts app."""

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username="user",
            password="Testuser1",
            first_name="User",
            last_name="Test",
            email="test@test.com"
        )
        
    def test_post_creation(self):
        """Test post creation."""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, "Test post")
        self.assertEqual(post.post_type, POST_TYPE_CHOICES[0][0])
        
        post2 = Post.objects.create(
            author=self.user,
            content="Test post 2",
            post_type=POST_TYPE_CHOICES[1][0],
            has_media=True,
            image=cloudinary.uploader.upload_image("static/images/phone.png")
        )
        self.assertEqual(post2.author, self.user)
        self.assertEqual(post2.content, "Test post 2")
        self.assertEqual(post2.post_type, POST_TYPE_CHOICES[1][0])
        self.assertEqual(post2.has_media, True)
        self.assertTrue('res.cloudinary.com' in post2.image.url)
        
    def test_comment_creation(self):
        """Test comment creation."""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "Test comment")
        
    def test_post_get_likes(self):
        """Test post.get_likes()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        self.assertEqual(post.get_likes(), 0)
        post.likes.add(self.user)
        self.assertEqual(post.get_likes(), 1)
        
    def test_post_get_dislikes(self):
        """Test post.get_dislikes()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        self.assertEqual(post.get_dislikes(), 0)
        post.dislikes.add(self.user)
        self.assertEqual(post.get_dislikes(), 1)
        
    def test_post_comments_count(self):
        """Test post.comments_count()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        self.assertEqual(post.comments_count(), 0)
        Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(post.comments_count(), 1)
        
    def test_post_get_comments(self):
        """Test post.get_comments()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertQuerysetEqual(post.get_comments(), Comment.objects.filter(post=post))
        Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment 2"
        )
        self.assertQuerysetEqual(post.get_comments(), Comment.objects.filter(post=post))
        
    def test_post_get_url(self):
        """Test post.get_url()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0],
            profile=self.user.profile
        )
        self.assertEqual(post.get_url(), f'/profiles/{self.user.username}/#post-{post.id}')
        
    def test_post_str(self):
        """Test post.__str__()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        self.assertEqual(str(post), post.content)
        
    def test_comment_get_likes(self):
        """Test comment.get_likes()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(comment.get_likes(), 0)
        comment.likes.add(self.user)
        self.assertEqual(comment.get_likes(), 1)
        
    def test_comment_get_dislikes(self):
        """Test comment.get_dislikes()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(comment.get_dislikes(), 0)
        comment.dislikes.add(self.user)
        self.assertEqual(comment.get_dislikes(), 1)
        
    def test_comment_get_url(self):
        """Test comment.get_url()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0],
            profile=self.user.profile
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(comment.get_url(), f'/profiles/{self.user.username}/#post-{comment.post.id}')
        
    def test_comment_str(self):
        """Test comment.__str__()"""
        post = Post.objects.create(
            author=self.user,
            content="Test post",
            post_type=POST_TYPE_CHOICES[0][0]
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content="Test comment"
        )
        self.assertEqual(str(comment), comment.content)
