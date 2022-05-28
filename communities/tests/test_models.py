"""Tests for the models of the communities app."""
from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import Community
from posts.models import Post
import datetime
import cloudinary
import cloudinary.uploader


class TestModels(TestCase):
    """Test models of the communities app."""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='user1',
            password='Testuser1',
            first_name='User1',
            last_name='Test',
            email='testuser@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testuser2',
            first_name='User2',
            last_name='Test',
            email='testuser2@example.com'
        )

    def test_community_creation(self):
        """Test community creation"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            bg_image='https://res.cloudinary.com/lexach91/image/upload/'
            'v1652420327/community_bg_images/mnf2mkql05rdtpm8r7r4.jpg',
            logo='https://res.cloudinary.com/lexach91/image/upload/'
            'v1652425017/community_logos/d3ubcbac1ws1xrsr2koj.png',
            creator=self.user1
        )
        community.members.add(self.user1)
        self.assertEqual(community.members.count(), 1)
        self.assertEqual(community.members.first(), self.user1)
        self.assertEqual(community.name, 'Test community')
        self.assertEqual(community.description, 'Test description')
        self.assertEqual(
            community.bg_image, 'https://res.cloudinary.com/lexach91/image/'
            'upload/v1652420327/community_bg_images/'
            'mnf2mkql05rdtpm8r7r4.jpg')
        self.assertEqual(
            community.logo, 'https://res.cloudinary.com/lexach91/image/upload/'
            'v1652425017/community_logos/d3ubcbac1ws1xrsr2koj.png')
        self.assertEqual(community.creator, self.user1)
        self.assertEqual(community.slug, 'test-community')

    def test_community_member_count_property(self):
        """Test community member count property"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            creator=self.user1
        )
        community.members.add(self.user1)
        self.assertEqual(community.member_count, 1)
        community.members.add(self.user2)
        self.assertEqual(community.member_count, 2)
        community.members.remove(self.user1)
        self.assertEqual(community.member_count, 1)
        community.members.remove(self.user2)
        self.assertEqual(community.member_count, 0)

    def test_community_get_posts_property(self):
        """Test community get posts property"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            creator=self.user1
        )
        community.members.add(self.user1)
        for i in range(10):
            post = Post.objects.create(
                author=self.user1,
                content='Test post',
                community=community,
                post_type=2,
            )
            post.save()
        self.assertEqual(community.get_posts.count(), 10)
        posts_by_filter = Post.objects.filter(community=community)
        posts_by_property = community.get_posts
        self.assertEqual(posts_by_filter.count(), posts_by_property.count())
        for post in posts_by_filter:
            self.assertIn(post, posts_by_property)

    def test_logo_url_propery(self):
        """Test getting community logo url"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            creator=self.user1
        )
        self.assertEqual(community.logo_url, '/static/images/default-logo.png')
        # upload logo to CloudinaryField
        community.logo = cloudinary.uploader.upload_image(
            'static/images/default-logo.png')
        self.assertTrue('res.cloudinary.com' in community.logo_url)

    def test_bg_image_url_property(self):
        """Test getting community bg image url"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            creator=self.user1
        )
        self.assertEqual(community.bg_image_url,
                         '/static/images/default-bg.jpg')
        # upload bg image to CloudinaryField
        community.bg_image = cloudinary.uploader.upload_image(
            'static/images/default-bg.jpg')
        self.assertTrue('res.cloudinary.com' in community.bg_image_url)

    def test_first_six_members_property(self):
        """Test getting first six members"""
        community = Community.objects.create(
            name='Test community',
            description='Test description',
            creator=self.user1
        )
        self.assertEqual(community.first_six_members.count(), 0)
        community.members.add(self.user1)
        self.assertEqual(community.first_six_members.count(), 1)
        community.members.add(self.user2)
        self.assertEqual(community.first_six_members.count(), 2)
        for i in range(6):
            user = User.objects.create_user(
                username='user{}'.format(i+3),
                password='Testuser{}'.format(i+3),
                first_name='User{}'.format(i+3),
                last_name='Test',
                email='test{}@test.com'.format(i+3)
            )
            community.members.add(user)
        self.assertEqual(community.members.count(), 8)
        self.assertEqual(community.first_six_members.count(), 6)
