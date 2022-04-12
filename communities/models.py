from turtle import update
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    description = models.TextField(blank=True)
    bg_image = CloudinaryField(
        'community_bg_image',
        folder = 'community_bg_images',
        null = True,
        blank = True
    )
    logo = CloudinaryField(
        'community_logo',
        folder = 'community_logos',
        null = True,
        blank = True
    )
    members = models.ManyToManyField(User, related_name='communities')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        return self.members.count()

    @property
    def get_posts(self):
        return self.posts.all()
    
    @property
    def get_slug(self):
        return self.name.replace(' ', '-')