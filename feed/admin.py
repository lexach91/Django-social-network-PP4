from django.contrib import admin
from .models import (
    PostEvent,
    CommentEvent,
    LikeDislikeEvent,
    FriendEvent,
    FriendRequestDeclinedEvent,
    FriendRequestEvent,
    RemoveFriendEvent,
    CommunityCreateEvent,
    CommunityDeleteEvent,
    CommunityJoinEvent,
    CommunityLeaveEvent,
)


@admin.register(PostEvent)
class PostEventAdmin(admin.ModelAdmin):
    """PostEvent model admin page configuration"""
    list_display = ('initiator', 'post', 'timestamp')
    list_filter = ['initiator']


@admin.register(CommentEvent)
class CommentEventAdmin(admin.ModelAdmin):
    """CommentEvent model admin page configuration"""
    list_display = ('initiator', 'post', 'comment', 'timestamp')
    list_filter = ['initiator']


@admin.register(LikeDislikeEvent)
class LikeDislikeEventAdmin(admin.ModelAdmin):
    """LikeDislikeEvent model admin page configuration"""
    list_display = ('initiator', 'post', 'comment', 'timestamp', 'like')
    list_filter = ('initiator', 'like')


@admin.register(FriendEvent)
class FriendEventAdmin(admin.ModelAdmin):
    """FriendEvent model admin page configuration"""
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(FriendRequestDeclinedEvent)
class FriendRequestDeclinedEventAdmin(admin.ModelAdmin):
    """FriendRequestDeclinedEvent model admin page configuration"""
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(FriendRequestEvent)
class FriendRequestEventAdmin(admin.ModelAdmin):
    """FriendRequestEvent model admin page configuration"""
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(RemoveFriendEvent)
class RemoveFriendEventAdmin(admin.ModelAdmin):
    """RemoveFriendEvent model admin page configuration"""
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(CommunityCreateEvent)
class CommunityCreateEventAdmin(admin.ModelAdmin):
    """CommunityCreateEvent model admin page configuration"""
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']


@admin.register(CommunityDeleteEvent)
class CommunityDeleteEventAdmin(admin.ModelAdmin):
    """CommunityDeleteEvent model admin page configuration"""
    list_display = ('initiator',  'timestamp')
    list_filter = ['initiator']


@admin.register(CommunityJoinEvent)
class CommunityJoinEventAdmin(admin.ModelAdmin):
    """CommunityJoinEvent model admin page configuration"""
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']


@admin.register(CommunityLeaveEvent)
class CommunityLeaveEventAdmin(admin.ModelAdmin):
    """CommunityLeaveEvent model admin page configuration"""
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']
