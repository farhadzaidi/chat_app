from django.urls import re_path
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.PublicChatConsumer.as_asgi()),
    re_path(r'ws/private-chat/(?P<room_name>\w+)/$', consumers.PrivateChatConsumer.as_asgi()),
]