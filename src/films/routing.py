# chats/routing.py
from django.conf.urls import url

from . import consumers_sync, consumers_async


websocket_urlpatterns = [
    url(r'^ws/films/async/(?P<room_name>[^/]+)/$', consumers_async.ChatConsumer),
    url(r'^ws/films/sync/(?P<room_name>[^/]+)/$', consumers_sync.ChatConsumer),
]
