from rest_framework import serializers
from .models import Relay10, Relay6, Device


class Relay6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay6
        fields = "__all__"
        read_only_fields = ("id", "device_id", "user")


class Relay10Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay10
        fields = "__all__"
        read_only_fields = ("id", "device_id", "user")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class Relay10Details(serializers.ModelSerializer):
    class Meta:
        model = Relay10
        fields = "__all__"
        read_only_fields = ("id", "user")

    def to_representation(self, instance):
        active_device = []
        free_device = []
        for i in range(1, 11):
            device_attr = getattr(instance, f"device_r{i}", None)
            if not device_attr:
                free_device.append(i)
        for i in range(1, 11):
            device_attr = getattr(instance, f"device_r{i}", None)
            if device_attr:
                device_name = getattr(instance, f"name{i}", "")
                device_state = getattr(instance, f"r{i}", "")
                device_representation = {
                    "device": DeviceSerializer(device_attr).data,
                    "name": device_name,
                    "state": device_state,
                    "relay_number": i,
                }
                active_device.append(device_representation)
        response = {
            "active_device": active_device,
            "id": instance.id,
            "type": "relay10",
            "device_id": instance.device_id,
            "state": instance.state,
            "free_device": free_device,
        }
        return response


class Relay6Details(serializers.ModelSerializer):
    class Meta:
        model = Relay6

    fields = "__all__"
    read_only_fields = ("id", "user")

    def to_representation(self, instance):
        active_device = []
        free_device = []
        for i in range(1, 7):
            device_attr = getattr(instance, f"device_r{i}", None)
            if not device_attr:
                free_device.append(i)
        for i in range(1, 7):
            device_attr = getattr(instance, f"device_r{i}", None)
            if device_attr:
                device_name = getattr(instance, f"name{i}", "")
                device_state = getattr(instance, f"r{i}", "")
                device_representation = {
                    "device": DeviceSerializer(device_attr).data,
                    "name": device_name,
                    "state": device_state,
                    "relay_number": i,
                }
                active_device.append(device_representation)
        response = {
            "active_device": active_device,
            "id": instance.id,
            "type": "relay6",
            "device_id": instance.device_id,
            "state": instance.state,
            "free_device": free_device,
        }
        return response


class AddDeviceSerializer(serializers.Serializer):
    port = serializers.IntegerField()
    device = serializers.UUIDField()
    name = serializers.CharField(max_length=39)

    def create(self, validated_data):
        device_id = self.context.get("device_id")
        device = Device.objects.get(id=self.data["device"])
        if Relay10.objects.filter(device_id=device_id).exists():
            relay = Relay10.objects.get(device_id=device_id)
        else:
            relay = Relay6.objects.get(device_id=device_id)
        setattr(relay, f'device_r{self.data["port"]}', device)
        setattr(relay, f'name{self.data["port"]}', self.data["name"])
        relay.save()
        return relay
