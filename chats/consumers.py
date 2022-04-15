import json
from channels.generic.websocket import AsyncWebsocketConsumer


# consumer for one-to-one chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room should be for two users only
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
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
        
        await self.close()
        