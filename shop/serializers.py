from rest_framework import serializers
from shop.models import (
    Shop,
    Machine,
    MaintenanceLogEntry,
    MaintenanceScheduleItem,
)


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

    class Meta:
        model = MaintenanceLogEntry
        fields = [
            'pk',
            'due_date',
            'item',
            'interval',
            'item_name',
            'machine_name',
            'description',
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
            'maintenance_items'
        ]


class shopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'pk',
            'name',
        ]
