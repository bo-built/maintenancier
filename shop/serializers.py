from rest_framework import serializers
from shop.models import (
    Shop,
    ShopUser,
    Machine,
    MaintenanceLogEntry,
    MaintenanceScheduleItem,
)


class shopUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopUser
        fields = [
            'pk',
            'name',
            'api_url',
        ]


class maintenanceScheduleItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceScheduleItem
        fields = [
            'pk',
            'name',
            'description',
            'source',
        ]


class maintenanceScheduleItemMicroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceScheduleItem
        fields = [
            'pk',
        ]


class maintenanceLogEntrySerializer(serializers.HyperlinkedModelSerializer):

    item = maintenanceScheduleItemMicroSerializer()
    done_by = shopUserSerializer()

    class Meta:
        model = MaintenanceLogEntry
        fields = [
            'pk',
            'due_date',
            'done_by',
            'done_date',
            'status',
            'item',
            'interval',
            'item_name',
            'machine_name',
            'description',
            'api_url',
        ]


class machineSerializer(serializers.HyperlinkedModelSerializer):
    maintenance_items = maintenanceScheduleItemSerializer(
        many=True,
    )

    class Meta:
        model = Machine
        fields = [
            'pk',
            'name',
            'api_url',
            'maintenance_items',
        ]


class shopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'pk',
            'name',
            'shop_api_url',
            'machine_api_url',
            'schedule_api_url',
            'shopuser_list_api_url',
            'shopuser_api_url',
        ]
