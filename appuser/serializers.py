from rest_framework import serializers
from appuser.models import User


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
        ]


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
