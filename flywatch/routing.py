from django.urls import re_path
from flywatch.consumers import FlywatchConsumer

websocket_urlpatterns = [
    re_path(r'ws/flywatch/$', FlywatchConsumer.as_asgi()),  # WebSocket endpoint
]
