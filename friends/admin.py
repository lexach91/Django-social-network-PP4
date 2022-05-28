from django.contrib import admin
from .models import FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_profile', 'to_profile')
    list_filter = ['from_profile', 'to_profile']
