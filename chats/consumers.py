import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


# consumer for one-to-one chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # @database_sync_to_async
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chatId']
        print(message)
        print(username)
        print(chat_id)
        
        message = await self.save_message(message, username, chat_id)
        print(message)
        avatar_url = await self.get_avatar_url(username)
        profile = await self.get_profile(username)
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'content': message.content,
                    # timestamp should be in format like 'April 19, 2022, 7:54 a.m.'
                    'timestamp': message.created_at.strftime('%B %d, %Y, %I:%M %p'),
                    },
                'author': {
                    'username': str(profile),
                    'avatar': avatar_url,
                    },
                'chatId': chat_id,
                'sendBy': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        send_by = event['sendBy']
        # chat_id = event['chatId']
        print(message)
        print(author)
        # print(chat_id)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'sendBy': send_by,
            # 'chatId': chat_id,
        }))
        
    # function to save message to database
    @database_sync_to_async
    def save_message(self, message, username, chat_id):
        chat = Chat.objects.get(id=chat_id)
        author = User.objects.get(username=username)
        content = message
        
        new_message = Message.objects.create(
            chat=chat,
            author=author,
            content=content
        )
        
        new_message.save()
        return new_message

    @database_sync_to_async
    def get_avatar_url(self, username):
        user = User.objects.get(username=username)
        return user.profile.avatar.url if user.profile.avatar else None
    
    @database_sync_to_async
    def get_profile(self, username):
        profile = User.objects.get(username=username).profile
        return profile