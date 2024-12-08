# flywatch/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from flywatch.routing import websocket_urlpatterns  # Import the routing from your app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flywatch.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Use the WebSocket URL routing
        )
    ),
})
