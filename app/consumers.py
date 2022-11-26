import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message
from asgiref.sync import sync_to_async
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_split = message.split('@@@')
        if message_split[0] == 'SYSTEM':
            self.user.username = 'SYSTEM'
            message = message_split[1]
        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'room': self.room_name,
                'datetime': now.isoformat(),
            }
        )
        message = Message(user=self.user.username, room=self.room_name, date=now.isoformat(), message=message)
        sync_to_async(message.save())

    async def chat_message(self, event):
        print(json.dumps(event))
        await self.send(text_data=json.dumps(event))
