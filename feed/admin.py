from django.contrib import admin
from .models import PostEvent, CommentEvent, LikeDislikeEvent

# Register your models here.
admin.site.register(PostEvent)
admin.site.register(CommentEvent)
admin.site.register(LikeDislikeEvent)