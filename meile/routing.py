# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/meile/$', consumers.ChatConsumer.as_asgi()),
]