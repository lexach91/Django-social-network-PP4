from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import date
from django.core.cache import cache
import datetime
from social_network import settings
from chats.models import Message


class Profile(models.Model):
    """Profile model"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = CloudinaryField(
        'avatar',
        folder='avatars',
        null=True,
        blank=True
    )
    birth_date = models.DateField(
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=25,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=25,
        blank=True,
        null=True
    )
    friends = models.ManyToManyField(
        'self',
        blank=True,
        related_name='friends'
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    bio = models.TextField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        """Profile model string representation"""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        return self.user.username

    @property
    def avatar_url(self):
        """Returns either profile's avatar url or the default avatar url"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default_avatar.svg'

    @property
    def age(self):
        """Calculates and returns the age of the user"""
        if self.birth_date:
            today = date.today()
            return (
                today.year -
                self.birth_date.year -
                ((today.month, today.day) <
                 (self.birth_date.month, self.birth_date.day))
            )
        return None

    @property
    def location(self):
        """Returns the user's location if it exists"""
        if self.country and self.city:
            return f'{self.country}, {self.city}'
        if self.country:
            return self.country
        if self.city:
            return self.city
        return None

    @property
    def pending_friends_in(self):
        """Returns the list of pending incoming friend requests"""
        profiles_list = []
        for friend_request in self.friend_request_to_profile.all():
            if not friend_request.accepted and not friend_request.declined:
                profiles_list.append(friend_request.from_profile)
        return profiles_list

    @property
    def pending_requests_count(self):
        """Returns the number of pending friend requests"""
        return len(self.pending_friends_in)

    @property
    def pending_friends_out(self):
        """Returns the list of pending outgoing friend requests"""
        profiles_list = []
        for friend_request in self.friend_request_from_profile.all():
            if not friend_request.accepted and not friend_request.declined:
                profiles_list.append(friend_request.to_profile)
        return profiles_list

    @property
    def unread_messages_count(self):
        """Returns the number of unread messages for the user"""
        messages = Message.objects.filter(
            chat__members=self.user,
            is_read=False
        ).exclude(
            author=self.user
        ).count()
        return messages

    def last_seen(self):
        """Returns the last time the user was seen"""
        return cache.get('seen_%s' % self.user.username)

    @property
    def online(self):
        """Returns True if the user was seen in the last 5 minutes"""
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
