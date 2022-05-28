from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils.text import slugify


class Community(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=False)
    description = models.TextField(max_length=100, blank=True)
    bg_image = CloudinaryField(
        'community_bg_image',
        folder='community_bg_images',
        null=True,
        blank=True
    )
    logo = CloudinaryField(
        'community_logo',
        folder='community_logos',
        null=True,
        blank=True
    )
    members = models.ManyToManyField(User, related_name='communities')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_communities')
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
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return '/static/images/default-logo.png'

    @property
    def bg_image_url(self):
        if self.bg_image:
            return self.bg_image.url
        return '/static/images/default-bg.jpg'

    @property
    def first_six_members(self):
        return self.members.all()[:6]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
