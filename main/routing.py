from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/product/(?P<product_id>\d+)/$', consumers.ProductConsumer.as_asgi()),
    re_path(r'ws/products/$', consumers.ProductListConsumer.as_asgi()),
]