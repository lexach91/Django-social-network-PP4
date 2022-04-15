import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth.models import User


# consumer for one-to-one chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = Chat.objects.get_or_create(id=self.chat_id)
        self.chat.members.add(self.user)
        self.chat.save()
        self.room_group_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(str(text_data))
        message = text_data_json['message']
        author = self.user
        chat = self.chat
        message = Message.objects.create(author=author, chat=chat, content=message)
        if text_data_json['has_media']:
            message.has_media = True
            message.image = text_data_json['image'] if text_data_json['image'] else None
            message.video = text_data_json['video'] if text_data_json['video'] else None
        message.save()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'author': message.author.username,
                'has_media': message.has_media,
                'image': message.image.url if message.image else None,
                'video': message.video.url if message.video else None,
                'created_at': message.created_at.strftime('%d %b %Y %H:%M:%S')
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        has_media = event['has_media']
        image = event['image']
        video = event['video']
        created_at = event['created_at']
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'has_media': has_media,
            'image': image,
            'video': video,
            'created_at': created_at
        }))