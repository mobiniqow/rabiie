from rest_framework import serializers

from .models import Room, RoomDevice


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = "__all__"
