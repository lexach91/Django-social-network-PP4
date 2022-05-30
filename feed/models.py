from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment


class PostEvent(models.Model):
    """PostEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_post_events',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "post"

    def __str__(self):
        """PostEvent model string representation"""
        if self.post.profile:
            if self.initiator == self.post.profile.user:
                name = str(self.initiator.profile)
                return f'{name} created a post in their profile'
            else:
                name1 = str(self.initiator.profile)
                name2 = str(self.post.profile.user.profile)
                return f'{name1} created a post in profile of {name2}'
        else:
            name = str(self.initiator.profile)
            community = str(self.post.community)
            return f'{name} created a post in community {community}'

    class Meta:
        """PostEvent model meta"""
        ordering = ['-timestamp']


class CommentEvent(models.Model):
    """CommentEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_comment_events',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment_events',
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_events'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "comment"

    def __str__(self):
        """CommentEvent model string representation"""
        return f'{self.initiator.profile} commented on {self.post}'

    class Meta:
        """CommentEvent model meta"""
        ordering = ['-timestamp']


class LikeDislikeEvent(models.Model):
    """LikeDislikeEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_like_dislike_events',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='like_dislike_events',
        blank=True,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='like_dislike_events',
        blank=True,
        null=True,
    )
    like = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "like_dislike"

    def __str__(self):
        """LikeDislikeEvent model string representation"""
        if self.post:
            if self.like:
                return f'{self.initiator.profile} liked {self.post}'
            else:
                return f'{self.initiator.profile} disliked {self.post}'
        else:
            if self.like:
                return f'{self.initiator.profile} liked {self.comment}'
            else:
                return f'{self.initiator.profile} disliked {self.comment}'

    class Meta:
        """LikeDislikeEvent model meta"""
        ordering = ['-timestamp']


class FriendRequestEvent(models.Model):
    """FriendRequestEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_friend_request_events',
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='targeted_friend_request_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "friend_request"

    def __str__(self):
        """FriendRequestEvent model string representation"""
        name1 = str(self.initiator.profile)
        name2 = str(self.target.profile)
        return f'{name1} sent a friend request to {name2}'

    class Meta:
        """FriendRequestEvent model meta"""
        ordering = ['-timestamp']


class FriendEvent(models.Model):
    """FriendEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_friend_events',
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='targeted_friend_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "friend_added"

    def __str__(self):
        """FriendEvent model string representation"""
        name1 = str(self.initiator.profile)
        name2 = str(self.target.profile)
        return f'{name1} and {name2} are now friends'

    class Meta:
        """FriendEvent model meta"""
        ordering = ['-timestamp']


class FriendRequestDeclinedEvent(models.Model):
    """FriendRequestDeclinedEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_friend_request_declined_events',
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='targeted_friend_request_declined_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "friend_request_declined"

    class Meta:
        """FriendRequestDeclinedEvent model meta"""
        ordering = ['-timestamp']


class RemoveFriendEvent(models.Model):
    """RemoveFriendEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_remove_friend_events',
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='targeted_remove_friend_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "friend_removed"

    def __str__(self):
        """RemoveFriendEvent model string representation"""
        name1 = str(self.initiator.profile)
        name2 = str(self.target.profile)
        return f'{name1} and {name2} are no longer friends'

    class Meta:
        """RemoveFriendEvent model meta"""
        ordering = ['-timestamp']


class CommunityJoinEvent(models.Model):
    """CommunityJoinEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_community_join_events',
    )
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        related_name='community_join_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "community_join"

    def __str__(self):
        """CommunityJoinEvent model string representation"""
        name = str(self.initiator.profile)
        community = str(self.community)
        return f'{name} joined community {community}'

    class Meta:
        """CommunityJoinEvent model meta"""
        ordering = ['-timestamp']


class CommunityLeaveEvent(models.Model):
    """CommunityLeaveEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_community_leave_events',
    )
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        related_name='community_leave_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "community_leave"

    def __str__(self):
        """CommunityLeaveEvent model string representation"""
        return f'{self.initiator.profile} left community {self.community.name}'

    class Meta:
        """CommunityLeaveEvent model meta"""
        ordering = ['-timestamp']


class CommunityCreateEvent(models.Model):
    """CommunityCreateEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_community_create_events',
    )
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        related_name='community_create_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "community_create"

    def __str__(self):
        """CommunityCreateEvent model string representation"""
        name = str(self.initiator.profile)
        community = str(self.community)
        return f'{name} created community {community}'

    class Meta:
        """CommunityCreateEvent model meta"""
        ordering = ['-timestamp']


class CommunityDeleteEvent(models.Model):
    """CommunityDeleteEvent model"""
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_community_delete_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = "community_delete"

    def __str__(self):
        """CommunityDeleteEvent model string representation"""
        return f'{self.initiator.profile} deleted community'

    class Meta:
        """CommunityDeleteEvent model meta"""
        ordering = ['-timestamp']
