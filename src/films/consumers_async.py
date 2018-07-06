# films/consumers.py
# this is async version
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message

from django.conf import settings
from django.contrib.auth.models import User

from datetime import datetime

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chats_{self.room_name}'

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
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now_time = datetime.now().strftime(settings.DATETIME_FORMAT)
        user = str(self.scope['user'])
        
        if not self.scope['user'].is_authenticated:
            try:
                user = User.objects.get(username='guest')
            except Exception as e:
                user = user.objects.create_user('guest', '', '12345678')
        else:
            user = self.scope['user']
        
        if not message:
            return

        Message.objects.create(
            user=user,
            message=message,
            group_name=self.room_group_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': str(user),
                'now_time': now_time,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user = event['user']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
        }))
