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
    path(
        'shop/<int:shop_pk>/machine/<int:machine_pk>/',
        views.MachineDashboard.as_view(),
        name='machine_dashboard',
    ),
]
