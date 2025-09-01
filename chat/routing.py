from django.urls import re_path

from chat.consumers import EchoConsumer, GlobalChatConsumer,DMChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/echo/', EchoConsumer.as_asgi()),
    re_path(r'ws/chat/global/', GlobalChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', DMChatConsumer.as_asgi()),
]