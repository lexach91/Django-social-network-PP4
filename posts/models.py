from click import edit
from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from communities.models import Community
from cloudinary.models import CloudinaryField


POST_TYPE_CHOICES = (
    (1, 'profile_wall'),
    (2, 'community_wall'),
)

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
    )
    content = models.TextField(max_length=500)
    image = CloudinaryField(
        'post_image',
        folder = 'posts',
        null = True,
        blank = True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    post_type = models.IntegerField(choices=POST_TYPE_CHOICES)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']