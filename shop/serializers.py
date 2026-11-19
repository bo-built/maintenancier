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
    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MaintenanceScheduleItem
        fields = [
            'pk',
            'name',
            'description',
            'source',
            'interval',
            'display_interval',
            'start_date',
            'machine',
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
            'machine_pk',
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
            'dashboard_url',
            'maintenance_history_api',
            'shop_schedule_api_url',
            'maintenance_items',
        ]


class shopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'pk',
            'name',
            'shop_dashboard_url',
            'shop_api_url',
            'machine_api_url',
            'schedule_api_url',
            'shopuser_list_api_url',
            'shopuser_api_url',
        ]
