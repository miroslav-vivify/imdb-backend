from channels.generic.websocket import AsyncWebsocketConsumer

class MovieEventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'{self.room_name}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def movie_comment(self, event):
        await self.send(event['data'])

    async def reaction(self, event):
        await self.send(event['data'])

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        pass 
