from rest_framework import serializers

from device.models import KeyedDevice


class KeyedDeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = KeyedDevice
        fields = "__all__"
