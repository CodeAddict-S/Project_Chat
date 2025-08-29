from channels.generic.websocket import AsyncWebsocketConsumer

class EchoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def disconnect(self, code):
        await self.disconnect()
    
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