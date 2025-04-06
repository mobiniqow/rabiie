from rest_framework import serializers
from .models import DeviceTimer


class DeviceTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTimer
        fields = "__all__"
    def create(self, validated_data):
        """
        override create method to set user
        """
        instance = super().create(validated_data)
        instance.user = self.context['request'].user
        instance.save()
        return instance