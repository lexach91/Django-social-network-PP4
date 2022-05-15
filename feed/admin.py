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

# Register your models here.
admin.site.register(PostEvent)
admin.site.register(CommentEvent)
admin.site.register(LikeDislikeEvent)
admin.site.register(FriendEvent)
admin.site.register(FriendRequestDeclinedEvent)
admin.site.register(FriendRequestEvent)
admin.site.register(RemoveFriendEvent)
admin.site.register(CommunityCreateEvent)
admin.site.register(CommunityDeleteEvent)
admin.site.register(CommunityJoinEvent)
admin.site.register(CommunityLeaveEvent)