import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Avg


class ProductConsumer(AsyncWebsocketConsumer):
    """WebSocket для сторінки окремого товару."""

    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.group_name = f'product_{self.product_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        data = await self.get_product_data()
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def product_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_product_data(self):
        from .models import Product, Favorite
        try:
            product = Product.objects.get(pk=self.product_id)
            avg_rating = product.ratings.aggregate(avg=Avg('score'))['avg']
            favorites_count = Favorite.objects.filter(product=product).count()
            return {
                'avg_rating': round(avg_rating, 1) if avg_rating else None,
                'favorites_count': favorites_count,
            }
        except Product.DoesNotExist:
            return {'avg_rating': None, 'favorites_count': 0}


class ProductListConsumer(AsyncWebsocketConsumer):
    """WebSocket для сторінки каталогу — оновлює рейтинги всіх товарів."""

    async def connect(self):
        self.group_name = 'product_list'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def list_update(self, event):
        await self.send(text_data=json.dumps(event['data']))