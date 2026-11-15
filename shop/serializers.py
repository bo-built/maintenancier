from rest_framework import serializers
from shop.models import (
    Shop,
)


class shopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'pk',
            'name',
        ]
