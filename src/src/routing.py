# films/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import films.routing


application = ProtocolTypeRouter({
    # Empty for now(http->django views added by default)
    # (http -> django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            films.routing.websocket_urlpatterns
        )
    ),
})
