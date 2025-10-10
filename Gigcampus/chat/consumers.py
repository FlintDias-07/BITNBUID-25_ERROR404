import json
from .models import Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'chat_{self.project_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('message', '').strip()
        username = data.get('username', 'Anonymous')
        user = self.scope["user"]
        project_id = self.project_id

        if not content:
            return

        # Save message to DB
        await self.save_message(user, project_id, content)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': content,
                'username': username
            }
        )

    @database_sync_to_async
    def save_message(self, user, project_id, content):
        from projects.models import Project
        project = Project.objects.get(id=project_id)
        Message.objects.create(
            project=project,
            sender=user,
            content=content
        )
