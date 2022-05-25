from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json



# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Chat between {" and ".join([member.username for member in self.members.all()])}'
    
    def get_last_message(self):
        return self.messages.last()
    
    def unread_messages_count(self):
        return self.messages.filter(is_read=False).count()
    
    class Meta:
        ordering = ['-last_message_at']
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content).replace('<br>', ' ')

    class Meta:
        ordering = ['created_at']
        
    # on save update chat's last_message_at and send notification
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.chat.last_message_at = self.created_at
        self.chat.save()
        
        channel_layer = get_channel_layer()
        receiver = self.chat.members.exclude(id=self.author.id)[0]
        receivers_unread_messages_count = Message.objects.filter(
            chat__members=receiver,
            is_read=False
        ).exclude(author=receiver).count()
        
        data = {
            'unread_messages': receivers_unread_messages_count,
        }
        async_to_sync(channel_layer.group_send)(
            f'notifications_{receiver.username}', {
                'type': 'send_notification',
                'data': data,
            }
        )
    
    @property
    def sent_at(self):
        now = datetime.now()
        diff = now - self.created_at.replace(tzinfo=None)
        seconds = diff.seconds
        days = diff.days
        months = days // 30
        years = days // 365
        minutes = seconds // 60
        hours = minutes // 60
        if years > 0:
            if years > 1:
                return '{} years ago'.format(years)
            else:
                return 'a year ago'
        elif months > 0:
            if months > 1:
                return '{} months ago'.format(months)
            else:
                return 'a month ago'
        elif days > 0:
            if days > 1:
                return '{} days ago'.format(days)
            else:
                return 'Yesterday'
        elif hours > 0:
            if hours > 1:
                return '{} hours ago'.format(hours)
            else:
                return 'an hour ago'
        elif minutes > 0:
            if minutes > 1:
                return '{} minutes ago'.format(minutes)
            else:
                return 'a minute ago'
        elif seconds > 0:
            if seconds >= 10:
                return '{} seconds ago'.format(seconds)
            else:
                return 'a few seconds ago'
        else:
            return 'just now'