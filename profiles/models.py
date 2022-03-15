from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import date

# Create your models here.
class Profile(models.Model):
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
        max_length=50,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    friends = models.ManyToManyField(
        'self',
        blank=True,
        related_name='friends'
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        return self.user.username

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
