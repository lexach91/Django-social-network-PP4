from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Chat between {self.members.all()[0]} and {self.members.all()[1]}'
    
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    has_media = models.BooleanField(default=False)
    image = CloudinaryField(
        'message_image',
        folder = 'messages',
        null = True,
        blank = True
    )
    video = CloudinaryField(
        'message_video',
        folder = 'messages',
        null = True,
        blank = True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
