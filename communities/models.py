from turtle import update
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='communities')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def member_count(self):
        return self.members.count()
