from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Signal to create profile for a user"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Signal to save profile for a user"""
    instance.profile.save()
