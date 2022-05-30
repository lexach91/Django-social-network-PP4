from django.apps import AppConfig
from django.db.models.signals import post_save


class ProfilesConfig(AppConfig):
    """Profiles app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    # when the app is ready, it will connect the signals to the models
    # and the signals will create the profile for each user that is created

    def ready(self):
        """Connect signals to models"""
        from profiles.signals import create_profile
        from django.contrib.auth.models import User
        post_save.connect(create_profile, sender=User)
        from profiles.signals import save_profile
        post_save.connect(save_profile, sender=User)
