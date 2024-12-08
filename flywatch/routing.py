# flywatch/routing.py

from django.urls import path
from flywatch.consumers import WebSocketConsumer

websocket_urlpatterns = [
    path('ws/socket/', WebSocketConsumer.as_asgi()),  # WebSocket endpoint
]
