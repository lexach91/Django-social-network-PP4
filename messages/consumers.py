import json
from channels.generic.websocket import AsyncWebsocketConsumer


# consumer for one-to-one chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass