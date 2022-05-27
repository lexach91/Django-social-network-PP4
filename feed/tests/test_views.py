"""Tests for the views of the feed app"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Comment
from communities.models import Community
from feed.models import (
    PostEvent,
    CommentEvent,
    LikeDislikeEvent,
    FriendEvent,
    FriendRequestEvent,
    FriendRequestDeclinedEvent,
    RemoveFriendEvent,
    CommunityJoinEvent,
    CommunityLeaveEvent,
    CommunityCreateEvent,   
    CommunityDeleteEvent,
)


class TestViews(TestCase):
    """Test views of the feed app."""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username="user1",
            password="Testuser1",
            first_name="User1",
            last_name="Test",
            email='test1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testuser2',
            first_name='User2',
            last_name='Test',
            email='test2@test.com'
        )
        self.client = Client()
        self.feed_url = reverse('feed')
        
    def test_feed_view_without_events(self):
        """Test feed view with no events"""
        self.client.login(username='user1', password='Testuser1')
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed/feed.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertEqual(len(response.context['events']), 0)
        
    def test_feed_view_with_events(self):
        """Test feed view with events"""
        self.client.login(username='user1', password='Testuser1')
        post = Post.objects.create(
            content="Test content",
            author=self.user1,
            post_type=1,
            profile=self.user1.profile
        )
        post_event = PostEvent.objects.create(
            post=post,
            initiator=self.user1,
        )
        comment = Comment.objects.create(
            content="Test comment",
            author=self.user1,
            post=post,
        )
        comment_event = CommentEvent.objects.create(
            comment=comment,
            initiator=self.user1,
            post=post,
        )
        like_dislike_event = LikeDislikeEvent.objects.create(
            post=post,
            initiator=self.user1,
            like=True,
        )
        friend_event = FriendEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        friend_request_declined_event = FriendRequestDeclinedEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        remove_friend_event = RemoveFriendEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        community = Community.objects.create(
            name="Test community",
            description="Test description",
            creator=self.user1,
        )
        community_join_event = CommunityJoinEvent.objects.create(
            community=community,
            initiator=self.user1,
        )        
        community_leave_event = CommunityLeaveEvent.objects.create(
            community=community,
            initiator=self.user1,
        )
        community_create_event = CommunityCreateEvent.objects.create(
            initiator=self.user1,
            community=community,
        )
        community_delete_event = CommunityDeleteEvent.objects.create(
            initiator=self.user1,
        )
        response = self.client.get(self.feed_url)
        self.assertEqual(len(response.context['events']), 10)
        self.assertTemplateUsed(response, 'feed/feed.html')
        self.assertEqual(response.context['user'], self.user1)
        self.assertTrue(post_event in response.context['events'])
        self.assertTrue(comment_event in response.context['events'])
        self.assertTrue(like_dislike_event in response.context['events'])
        self.assertTrue(friend_event in response.context['events'])
        self.assertTrue(friend_request_declined_event in response.context['events'])
        self.assertTrue(remove_friend_event in response.context['events'])
        self.assertTrue(community_join_event in response.context['events'])
        self.assertTrue(community_leave_event in response.context['events'])
        self.assertTrue(community_create_event in response.context['events'])
        self.assertTrue(community_delete_event in response.context['events'])
        