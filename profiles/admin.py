from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin page configuration"""
    list_display = (
        'user',
        'first_name',
        'last_name',
        'country',
        'city',
        'bio',
        'friends_count',
        'age',
    )
    list_filter = ['user', 'country', 'city']

    def friends_count(self, obj):
        return obj.friends.count()
    friends_count.short_description = 'Friends count'
