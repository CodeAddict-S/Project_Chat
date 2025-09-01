from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from .models import Chat
from django.conf import settings
import jwt

class EchoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def disconnect(self, code):
        pass

class GlobalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('global', self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        await self.channel_layer.group_send('global', {
            'type': 'callback_for_chat_message',
            'content': text_data
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard('global', self.channel_name)

    async def callback_for_chat_message(self, event):
        await self.send(text_data=event['content'])


User = get_user_model()
class DMChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        query_params = parse_qs(self.scope["query_string"].decode())
        token = query_params.get("token", [None])[0]

        if not token:
            await self.close()
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            self.user = await self.get_user(user_id)
        except Exception:
            await self.close()
            return

        if not self.user:
            await self.close()
            return

        chat_exists = await self.check_chat_exists(self.room_name, self.user.id)
        if not chat_exists:
            await self.close()
            return

        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "callback_for_chat_message",
                "content": text_data,
                "username": self.user.username,
            }
        )

    async def callback_for_chat_message(self, event):
        await self.send(text_data=event['content'])

    @staticmethod
    async def get_user(user_id):
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    async def check_chat_exists(room_name, user_id):
        try:
            chat = await Chat.objects.aget(name=room_name)
            return chat.user_1_id == user_id or chat.user_2_id == user_id
        except Chat.DoesNotExist:
            return False