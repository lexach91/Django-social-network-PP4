from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment


# Create your models here.
class PostEvent(models.Model):
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
    
    def __str__(self):
        if self.post.profile:
            if self.initiator == self.post.profile.user:
                return f'{self.initiator.profile} created a post in their profile'
            else:
                return f'{self.initiator.profile} created a post in profile of {self.post.profile}'
        else:
            return f'{self.initiator.profile} created a post in community {self.post.community.name}'
        
    class Meta:
        ordering = ['-timestamp']
        

class CommentEvent(models.Model):
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
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.initiator.profile} commented on {self.post}'
    
    class Meta:
        ordering = ['-timestamp']
        
        
class LikeDislikeEvent(models.Model):
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
    
    def __str__(self):
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
        ordering = ['-timestamp']
        
        
class FriendRequestEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} sent a friend request to {self.target.profile}'
    
    class Meta:
        ordering = ['-timestamp']
        

class FriendEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} and {self.target.profile} are now friends'
    
    class Meta:
        ordering = ['-timestamp']
        
        
class RemoveFriendEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} and {self.target.profile} are no longer friends'
    
    class Meta:
        ordering = ['-timestamp']
        

class CommunityJoinEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} joined community {self.community.name}'
    
    class Meta:
        ordering = ['-timestamp']
        
        
class CommunityLeaveEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} left community {self.community.name}'
    
    class Meta:
        ordering = ['-timestamp']
        
        
class CommunityCreateEvent(models.Model):
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
    
    def __str__(self):
        return f'{self.initiator.profile} created community {self.community.name}'
    
    class Meta:
        ordering = ['-timestamp']
        
class CommunityDeleteEvent(models.Model):
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_community_delete_events',
    )
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        related_name='community_delete_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.initiator.profile} deleted community {self.community.name}'
    
    class Meta:
        ordering = ['-timestamp']
        