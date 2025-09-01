from django.urls import re_path

from chat.consumers import EchoConsumer, GlobalChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/echo/', EchoConsumer.as_asgi()),
    re_path(r'ws/chat/global/', GlobalChatConsumer.as_asgi()),

]