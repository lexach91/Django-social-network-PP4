"""Tests for the models of the feed app."""
from django.test import TestCase
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


class TestModels(TestCase):
    """Test models of the feed app."""

    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username="user1",
            password="Testuser1",
            first_name="User1",
            last_name="Test",
            email="test1@test.com",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Testuser2",
            first_name="User2",
            last_name="Test",
            email="test2@test.comj",
        )

    def test_post_event_creation(self):
        """Test post event creation"""
        post = Post.objects.create(
            content="Test content",
            author=self.user1,
            post_type=1,
        )
        post_event = PostEvent.objects.create(
            post=post,
            initiator=self.user1,
        )
        self.assertEqual(post_event.post, post)
        self.assertEqual(post_event.initiator, self.user1)
        self.assertEqual(post_event.type, "post")

    def test_comment_event_creation(self):
        """Test comment event creation"""
        post = Post.objects.create(
            content="Test content",
            author=self.user1,
            post_type=1,
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
        self.assertEqual(comment_event.comment, comment)
        self.assertEqual(comment_event.initiator, self.user1)
        self.assertEqual(comment_event.type, "comment")
        self.assertEqual(comment_event.post, post)

    def test_like_dislike_event_creation(self):
        """Test like dislike event creation"""
        post = Post.objects.create(
            content="Test content",
            author=self.user1,
            post_type=1,
        )
        like_dislike_event = LikeDislikeEvent.objects.create(
            post=post,
            initiator=self.user1,
            like=True,
        )
        self.assertEqual(like_dislike_event.post, post)
        self.assertEqual(like_dislike_event.initiator, self.user1)
        self.assertEqual(like_dislike_event.type, "like_dislike")
        self.assertTrue(like_dislike_event.like)
        comment = Comment.objects.create(
            content="Test comment",
            author=self.user1,
            post=post,
        )
        like_dislike_event = LikeDislikeEvent.objects.create(
            comment=comment,
            initiator=self.user2,
            like=False,
        )
        self.assertEqual(like_dislike_event.comment, comment)
        self.assertEqual(like_dislike_event.initiator, self.user2)
        self.assertEqual(like_dislike_event.type, "like_dislike")
        self.assertFalse(like_dislike_event.like)

    def test_friend_event_creation(self):
        """Test friend event creation"""
        friend_event = FriendEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        self.assertEqual(friend_event.initiator, self.user1)
        self.assertEqual(friend_event.target, self.user2)
        self.assertEqual(friend_event.type, "friend_added")

    def test_friend_request_event_creation(self):
        """Test friend request event creation"""
        friend_request_event = FriendRequestEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        self.assertEqual(friend_request_event.initiator, self.user1)
        self.assertEqual(friend_request_event.target, self.user2)
        self.assertEqual(friend_request_event.type, "friend_request")

    def test_friend_request_declined_event_creation(self):
        """Test friend request declined event creation"""
        request_declined_event = FriendRequestDeclinedEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        self.assertEqual(request_declined_event.initiator, self.user1)
        self.assertEqual(request_declined_event.target, self.user2)
        self.assertEqual(request_declined_event.type,
                         "friend_request_declined")

    def test_remove_friend_event_creation(self):
        """Test remove friend event creation"""
        remove_friend_event = RemoveFriendEvent.objects.create(
            initiator=self.user1,
            target=self.user2,
        )
        self.assertEqual(remove_friend_event.initiator, self.user1)
        self.assertEqual(remove_friend_event.target, self.user2)
        self.assertEqual(remove_friend_event.type, "friend_removed")

    def test_community_join_event_creation(self):
        """Test community join event creation"""
        community = Community.objects.create(
            name="Test community",
            description="Test description",
            creator=self.user1,
        )
        community_join_event = CommunityJoinEvent.objects.create(
            community=community,
            initiator=self.user2,
        )
        self.assertEqual(community_join_event.community, community)
        self.assertEqual(community_join_event.initiator, self.user2)
        self.assertEqual(community_join_event.type, "community_join")

    def test_community_leave_event_creation(self):
        """Test community leave event creation"""
        community = Community.objects.create(
            name="Test community",
            description="Test description",
            creator=self.user1,
        )
        community_leave_event = CommunityLeaveEvent.objects.create(
            community=community,
            initiator=self.user2,
        )
        self.assertEqual(community_leave_event.community, community)
        self.assertEqual(community_leave_event.initiator, self.user2)
        self.assertEqual(community_leave_event.type, "community_leave")

    def test_community_create_event_creation(self):
        """Test community create event creation"""
        community = Community.objects.create(
            name="Test community",
            description="Test description",
            creator=self.user1,
        )
        community_create_event = CommunityCreateEvent.objects.create(
            initiator=self.user1,
            community=community,
        )
        self.assertEqual(community_create_event.initiator, self.user1)
        self.assertEqual(community_create_event.community, community)
        self.assertEqual(community_create_event.type, "community_create")

    def test_community_delete_event_creation(self):
        """Test community delete event creation"""
        community_delete_event = CommunityDeleteEvent.objects.create(
            initiator=self.user1,
        )
        self.assertEqual(community_delete_event.initiator, self.user1)
        self.assertEqual(community_delete_event.type, "community_delete")
