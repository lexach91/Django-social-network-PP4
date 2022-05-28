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
    list_display = ('initiator', 'post', 'timestamp')
    list_filter = ['initiator']


@admin.register(CommentEvent)
class CommentEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'post', 'comment', 'timestamp')
    list_filter = ['initiator']


@admin.register(LikeDislikeEvent)
class LikeDislikeEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'post', 'comment', 'timestamp', 'like')
    list_filter = ('initiator', 'like')


@admin.register(FriendEvent)
class FriendEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(FriendRequestDeclinedEvent)
class FriendRequestDeclinedEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(FriendRequestEvent)
class FriendRequestEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(RemoveFriendEvent)
class RemoveFriendEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'target', 'timestamp')
    list_filter = ['initiator', 'target']


@admin.register(CommunityCreateEvent)
class CommunityCreateEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']


@admin.register(CommunityDeleteEvent)
class CommunityDeleteEventAdmin(admin.ModelAdmin):
    list_display = ('initiator',  'timestamp')
    list_filter = ['initiator']


@admin.register(CommunityJoinEvent)
class CommunityJoinEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']


@admin.register(CommunityLeaveEvent)
class CommunityLeaveEventAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'community', 'timestamp')
    list_filter = ['initiator', 'community']
