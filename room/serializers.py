from rest_framework import serializers
from .models import Room, RoomDevice


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().update(instance, validated_data)


class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = "__all__"
