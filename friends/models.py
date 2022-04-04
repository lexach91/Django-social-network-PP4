from turtle import update
from django.db import models
from profiles.models import Profile

# Create your models here.
class FriendRequest(models.Model):
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
        return f'{self.from_profile} to {self.to_profile}'
    
    def accept(self):
        self.accepted = True
        self.save()
        
    def decline(self):
        self.declined = True
        self.save()
    
    def is_accepted(self):
        return self.accepted
    
    def is_declined(self):
        return self.declined
    
    def is_pending(self):
        return not (self.accepted or self.declined)
    
    @classmethod
    def get_all_requests(self):
        return FriendRequest.objects.all()
    
    @classmethod
    def get_pending_requests(self):
        return FriendRequest.objects.filter(accepted=False, declined=False)
    