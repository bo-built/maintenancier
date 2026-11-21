from django.urls import path
from shop import api as api_views


app_name = 'shopapi'

urlpatterns = [
    path(
        'api/shop/',
        api_views.ShopApi.as_view(),
        name='shop_api',
    ),
    path(
        'api/shop/<int:shop_pk>/',
        api_views.ShopApi.as_view(),
        name='shop_detail_api',
    ),
    path(
        'api/shop/<int:shop_pk>/log/',
        api_views.MaintenanceScheduleApi.as_view(),
        name='maintenance_history_api',
    ),
    path(
        'api/shop/<int:shop_pk>/log/<int:machine_pk>/',
        api_views.MaintenanceScheduleApi.as_view(),
        name='maintenance_machine_history_api',
    ),
    path(
        'api/shop/<int:shop_pk>/machine/',
        api_views.MachineApi.as_view(),
        name='machine_api',
    ),
    path(
        'api/shop/<int:shop_pk>/machine/<int:machine_pk>/',
        api_views.MachineApi.as_view(),
        name='machine_detail_api',
    ),
    path(
        'api/shop/<int:shop_pk>/schedule/',
        api_views.MaintenanceScheduleApi.as_view(),
        name='maintenance_schedule_api',
    ),
    path(
        'api/shop/<int:shop_pk>/schedule/interval/<str:interval>/',
        api_views.MaintenanceScheduleApi.as_view(),
        name='maintenance_schedule_by_interval_api',
    ),
    path(
        'api/shop/<int:shop_pk>/schedule/<int:item_pk>/',
        api_views.MaintenanceScheduleApi.as_view(),
        name='maintenance_schedule_detail_api',
    ),
    path(
        'api/shop/<int:shop_pk>/schedule/<int:item_pk>/log/',
        api_views.LogEntryApi.as_view(),
        name='log_item_api',
    ),
    path(
        'api/shop/<int:shop_pk>/schedule/<int:item_pk>/log/<int:log_item_pk>/',
        api_views.LogEntryApi.as_view(),
        name='log_item_detail_api',
    ),
    path(
        'api/shop/<int:shop_pk>/user/',
        api_views.ShopUserApi.as_view(),
        name='shop_user_api',
    ),
    path(
        'api/shop/<int:shop_pk>/user/all/',
        api_views.ShopUserApi.as_view(),
        name='shop_user_list_api',
    ),
    path(
        'api/shop/<int:shop_pk>/user/<int:shop_user_pk>/',
        api_views.ShopUserApi.as_view(),
        name='shop_user_detail_api',
    ),
]
