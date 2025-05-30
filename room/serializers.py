from rest_framework import serializers

from device.serializers import DeviceSerializer, PsychrometerSerializer, Relay6Serializer, Relay10Serializer
from .models import Room, RoomDevice, RoomPicture


class RoomSerializer(serializers.ModelSerializer):
    axe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_axe(self, obj: Room):
        try:
            return str(obj.image.image.url)
        except Exception as e:
            return ""

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user
        return super().update(instance, validated_data)


class RoomDeviceSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True)
    device = DeviceSerializer(read_only=True)
    psychrometer = PsychrometerSerializer(read_only=True)
    relay_6 = Relay6Serializer(read_only=True)
    relay_8 = Relay10Serializer(read_only=True)
    class Meta:
        model = RoomDevice
        fields = "__all__"



class RoomPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPicture
        fields = "__all__"
