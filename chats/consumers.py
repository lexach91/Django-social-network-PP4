import json
from os import sync
from channels.generic.websocket import AsyncWebsocketConsumer
from sympy import content
from .models import Message, Chat
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async


# consumer for one-to-one chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['username']
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
        
        await self.save_message(message, username, chat_id)
                
        # first_user = self.user
        # second_user = User.objects.get(username=username)
        # chat = Chat.objects.filter(members=first_user).filter(members=second_user).first()
        # print(first_user, username)
        # print(message)
        # new_message = Message.objects.create(
        #     chat=chat,
        #     author=first_user,
        #     content=message
        # )
        # new_message.save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chatId': chat_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_id = event['chatId']
        print(message)
        print(username)
        print(chat_id)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chatId': chat_id
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