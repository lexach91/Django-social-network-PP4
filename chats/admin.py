from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """Chat model admin page configuration"""
    list_display = ('get_members', 'created_at',
                    'last_message_at', 'unread_messages_count')

    def get_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message model admin page configuration"""
    list_display = ('chat', 'author', 'content',
                    'is_read', 'created_at', 'updated_at')
    list_filter = ('chat', 'author', 'is_read')
