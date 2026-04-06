import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import properties.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homesathi.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            properties.routing.websocket_urlpatterns
        )
    ),
})