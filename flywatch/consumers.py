# flywatch/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FlywatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "flywatch_group"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_to_websocket(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
