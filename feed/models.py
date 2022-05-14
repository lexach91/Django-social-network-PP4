from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


# Create your models here.
class PostEvent(models.Model):
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_post_events',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_events',
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.post.profile:
            if self.initiator == self.post.profile.user:
                return f'{self.initiator.profile} created a post in their profile'
            else:
                return f'{self.initiator.profile} created a post in profile of {self.post.profile}'
        else:
            return f'{self.initiator.profile} created a post in community {self.post.community.name}'