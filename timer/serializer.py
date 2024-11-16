from rest_framework import serializers
from .models import DeviceTimer


class DeviceTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTimer
        fields = "__all__"
