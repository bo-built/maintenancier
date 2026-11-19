from django.urls import path
from shop import views


app_name = 'shop'


urlpatterns = [
    path(
        'dashboard/',
        views.Dashboard.as_view(),
        name='home',
    ),
    path(
        'shop/<int:shop_pk>/dashboard/',
        views.ShopDashboard.as_view(),
        name='shop_dashboard',
    ),
]
