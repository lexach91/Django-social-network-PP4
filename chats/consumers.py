import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    """Async websocket consumer to process chat messages"""
    async def connect(self):
        """Connect to chat group"""
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect from chat group"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        # message type is passed from js client
        event_type = text_data_json['type']
        if event_type == 'chat_message':  # regular chat message
            message = text_data_json['message']
            username = text_data_json['username']
            chat_id = text_data_json['chatId']

            message = await self.save_message(message, username, chat_id)
            avatar_url = await self.get_avatar_url(username)
            profile = await self.get_profile(username)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',  # call chat_message method
                    'message': {
                        'content': message.content,
                        'timestamp': message.created_at.strftime('%B %d, %Y,'
                                                                 '%I:%M %p'),
                    },
                    'author': {
                        'username': str(profile),
                        'avatar': avatar_url,
                    },
                    'chatId': chat_id,
                    'messageId': message.id,
                    'sendBy': username,
                }
            )
        elif event_type == 'typing':  # user is typing
            username = text_data_json['username']
            chat_id = text_data_json['chatId']
            profile = await self.get_profile(username)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing',  # call typing method
                    'username': username,
                    'profile_name': str(profile),
                    'chatId': chat_id,
                }
            )

    async def chat_message(self, event):
        """Processes chat message event"""
        event_type = event['type']
        if event_type == 'chat_message':
            message = event['message']
            author = event['author']
            send_by = event['sendBy']
            message_id = event['messageId']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'author': author,
                'sendBy': send_by,
                'messageId': message_id,
            }))

    async def typing(self, event):
        """Processes typing event"""
        event_type = event['type']
        if event_type == 'typing':
            username = event['username']
            profile_name = event['profile_name']
            chat_id = event['chatId']
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'username': username,
                'profile_name': profile_name,
                'chatId': chat_id,
            }))

    # functions to access database and get data asynchronously
    @database_sync_to_async
    def save_message(self, message, username, chat_id):
        """Saves message to database"""
        chat = Chat.objects.get(id=chat_id)
        author = User.objects.get(username=username)
        content = message

        new_message = Message.objects.create(
            chat=chat,
            author=author,
            content=content
        )

        return new_message

    @database_sync_to_async
    def get_avatar_url(self, username):
        """Returns avatar url of user's profile"""
        user = User.objects.get(username=username)
        return user.profile.avatar_url

    @database_sync_to_async
    def get_profile(self, username):
        """Returns user's profile"""
        profile = User.objects.get(username=username).profile
        return profile
