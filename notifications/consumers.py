import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected')
        self.user = self.scope['user']
        self.room_name = self.user.username
        self.room_group_name = f'notifications_{self.room_name}'
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()
            
    async def disconnect(self, close_code):
        print('disconnected')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # async def receive(self, text_data):
    #     await self.send(text_data=json.dumps({'message': 'Hello World!'}))
        
    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))