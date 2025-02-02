import json
from channels.generic.websocket import AsyncWebsocketConsumer
from flywatch.views import shared_dict  # Import the shared dictionary

class FlywatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Handle disconnection if needed

    async def receive(self, text_data):
        # Send the current `shared_dict` data to the client
        await self.send(json.dumps(shared_dict))
