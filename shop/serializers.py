from rest_framework import serializers
from shop.models import (
    Shop,
    ShopUser,
    Machine,
    LogEntry,
    MaintenanceTask,
)


class shopUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopUser
        fields = [
            'pk',
            'name',
            'api_url',
        ]


class LogEntryMicroSerializer(serializers.HyperlinkedModelSerializer):

    done_by = shopUserSerializer()

    class Meta:
        model = LogEntry
        fields = [
            'pk',
            'due_date',
            'done_by',
            'done_date',
            'status',
            'api_url',
        ]


class MaintenanceTaskSerializer(serializers.HyperlinkedModelSerializer):
    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        required=False,
        allow_null=True,
    )
    next_scheduled = LogEntryMicroSerializer()

    class Meta:
        model = MaintenanceTask
        fields = [
            'pk',
            'status',
            'name',
            'description',
            'source',
            'interval',
            'display_interval',
            'start_date',
            'machine',
            'api_url',
            'next_scheduled',
        ]


class MaintenanceTaskMicroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = [
            'pk',
        ]


class LogEntrySerializer(serializers.HyperlinkedModelSerializer):

    task = MaintenanceTaskMicroSerializer()
    done_by = shopUserSerializer()

    class Meta:
        model = LogEntry
        fields = [
            'pk',
            'due_date',
            'done_by',
            'done_date',
            'status',
            'notes',
            'task',
            'interval',
            'task_name',
            'machine_name',
            'machine_pk',
            'description',
            'api_url',
        ]


class machineSerializer(serializers.HyperlinkedModelSerializer):
    maintenance_items = MaintenanceTaskSerializer(
        many=True,
    )

    class Meta:
        model = Machine
        fields = [
            'pk',
            'name',
            'is_shop',
            'status',
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
