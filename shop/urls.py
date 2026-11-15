from django.urls import path
from shop import api as api_views

app_name = 'shop'

urlpatterns = [
    path(
        'api/shop/',
        api_views.shopApi.as_view(),
        name='shop_api',
    ),
    path(
        'api/shop/<int:pk>/',
        api_views.shopApi.as_view(),
        name='shop_detail_api',
    ),
]