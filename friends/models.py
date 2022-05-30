from django.db import models
from profiles.models import Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.


class FriendRequest(models.Model):
    """Friend Request model"""
    from_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_request_from_profile'
    )
    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_request_to_profile'
    )

    sent_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    def __str__(self):
        """Friend Request model string representation"""
        return f'{self.from_profile} to {self.to_profile}'

    def accept(self):
        """Accepts friend request"""
        self.accepted = True
        self.save()

    def decline(self):
        """Declines friend request"""
        self.declined = True
        self.save()

    def is_accepted(self):
        """Returns True if friend request is accepted"""
        return self.accepted

    def is_declined(self):
        """Returns True if friend request is declined"""
        return self.declined

    def is_pending(self):
        """Returns True if friend request is pending"""
        return not (self.accepted or self.declined)

    @classmethod
    def get_all_requests(self):
        """Class method to get all friend requests"""
        return FriendRequest.objects.all()

    @classmethod
    def get_pending_requests(self):
        """Class method to get all pending friend requests"""
        return FriendRequest.objects.filter(accepted=False, declined=False)

    def save(self, *args, **kwargs):
        """Saves friend request and sends notification to target user"""
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        receiver = self.to_profile.user

        data = {
            'pending_requests': receiver.profile.pending_requests_count,
        }

        async_to_sync(channel_layer.group_send)(
            f'notifications_{receiver.username}', {
                'type': 'send_notification',
                'data': data,
            }
        )
