from rest_framework import serializers
from django.shortcuts import get_object_or_404

from room.models import Room, RoomDevice
from .models import Relay10, Relay6, Device, Psychrometer


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

class PsychrometerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychrometer
        fields = '__all__'

    def create(self, validated_data):
        # اگر نیاز به اعمال تغییرات اضافی دارید می‌توانید در اینجا انجام دهید
        return Psychrometer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # اگر نیاز به اعمال تغییرات اضافی برای آپدیت دارید می‌توانید در اینجا انجام دهید
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AddPsychrometerToRelay6Serializer(serializers.Serializer):
    port = serializers.IntegerField()
    psychrometer = PsychrometerSerializer()
    room_id = serializers.IntegerField(required=False)

    def validate_port(self, value):
        if value < 1 or value > 6:
            raise serializers.ValidationError("Port number must be between 1 and 6.")
        return value

    def create(self, validated_data):
        psychrometer_data = validated_data.pop("psychrometer")
        psychrometer = Psychrometer.objects.create(**psychrometer_data)

        relay6_id = self.context.get("relay6_id")
        relay = Relay6.objects.get(id=relay6_id)

        port = validated_data["port"]
        setattr(relay, f"t{port}", psychrometer)
        relay.save()

        room_id = validated_data.get("room_id")
        if room_id:
            try:
                room = Room.objects.get(id=room_id)
                RoomDevice.objects.create(room=room, psychrometer=psychrometer)
            except Room.DoesNotExist:
                raise serializers.ValidationError({"room_id": "Room not found"})

        # برای استفاده در to_representation ذخیره‌اش می‌کنیم
        self.psychrometer = psychrometer
        self.port = port
        self.room_id = room_id

        return psychrometer

    def to_representation(self, instance):
        return {
            "port": self.port,
            "psychrometer": PsychrometerSerializer(self.psychrometer).data,
            "room_id": self.room_id
        }
