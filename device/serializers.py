from rest_framework import serializers
from .models import Relay10, Relay6, Device


class Relay6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay6
        fields = '__all__'
        read_only_fields = ("id", "product_id", "user")


class Relay10Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay10
        fields = '__all__'
        read_only_fields = ("id", "product_id", "user")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
