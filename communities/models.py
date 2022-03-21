from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='communities')
    
    def __str__(self):
        return self.name
