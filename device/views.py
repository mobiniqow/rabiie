from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from django.db import transaction
from django.forms.models import model_to_dict

from device.models import Relay10, Relay6, Device, Psychrometer, PsychrometerImage
from device.serializers import (
    Relay10Serializer,
    Relay6Serializer,
    DeviceSerializer,
    Relay10Details,
    AddDeviceSerializer,
    Relay6Details, AddPsychrometerToRelay6Serializer, PsychrometerSerializer, PsychrometerImageSerializer,
)
from room.models import Room, RoomDevice


@api_view(("GET", "PATCH"))
def search_device(request, device_id):
    if request.method == "GET":
        devices = Relay10.objects.filter(device_id=device_id)
        if not devices.exists():
            devices = Relay6.objects.filter(device_id=device_id)
        if not devices.exists():
            return Response(
                {"message": "device not found"}, status=status.HTTP_404_NOT_FOUND
            )
        device = devices.first()
        device.reset()
        device.user = request.user
        device.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCH":
        devices = Relay10.objects.filter(device_id=device_id, user=request.user)
        if devices.exists():
            serializer = Relay10Serializer(
                devices.first(), data=request.data, partial=True
            )
        if not devices.exists():
            devices = Relay6.objects.filter(device_id=device_id, user=request.user)
            if devices.exists():
                serializer = Relay6Serializer(
                    devices.first(), data=request.data, partial=True
                )
        if not devices.exists():
            return Response(
                {"message": "object not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data})


@api_view(("PATCH", "GET"))
def search_device_socket(request, device_id):
    if request.method == "GET":
        devices = Relay10.objects.filter(device_id=device_id)
        if not devices.exists():
            devices = Relay6.objects.filter(device_id=device_id)
        if not devices.exists():
            return Response(
                {"message": "device not found"}, status=status.HTTP_404_NOT_FOUND
            )
        device = devices.first()
        device.reset()
        device.user = request.user
        device.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCH":
        devices = Relay10.objects.filter(device_id=device_id)
        if devices.exists():
            device = devices.first()
            serializer = Relay10Serializer(device, data=request.data, partial=True)
        else:
            devices = Relay6.objects.filter(device_id=device_id)
            if devices.exists():
                device = devices.first()
                serializer = Relay6Serializer(device, data=request.data, partial=True)
            else:
                return Response(
                    {"message": "object not found"}, status=status.HTTP_404_NOT_FOUND
                )

        serializer.is_valid(raise_exception=True)

        # مقادیر قبلی قبل از ذخیره
        old_data = model_to_dict(device, fields=[f"r{i}" for i in range(1, 11)])

        # ذخیره تغییرات
        instance = serializer.save()

        # مقادیر جدید بعد از ذخیره
        new_data = model_to_dict(instance, fields=[f"r{i}" for i in range(1, 11)])

        # پیدا کردن رله‌هایی که تغییر کرده‌اند
        changed_relays = [
            i for i in range(1, 11) if old_data.get(f"r{i}") != new_data.get(f"r{i}")
        ]

        # ارسال پیام فقط برای رله‌های تغییر کرده
        for relay_number in changed_relays:
            payload = instance.get_schedular_date(relay_number)
            message = Message(
                payload=payload,
                _type="WS",
                device_id=instance.device_id,
                # _datetime=instance.get_time(),
            )
            send_broker_message(message)

        return Response({"message": serializer.data})


@api_view(("PATCH", "POST"))
def client_device(request, device_id):
    try:
        with transaction.atomic():
            relay = None
            relay_type = None

            if Relay10.objects.filter(device_id=device_id).exists():
                relay = Relay10.objects.get(device_id=device_id)
                relay_type = "r10"
                serializer_class = Relay10Serializer
            elif Relay6.objects.filter(device_id=device_id).exists():
                relay = Relay6.objects.get(device_id=device_id)
                relay_type = "r6"
                serializer_class = Relay6Serializer
            else:
                return Response({"message": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

            # PATCH method
            if request.method == "PATCH":
                serializer = serializer_class(relay, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                room_id = request.data.get("room_id")
                if room_id:
                    try:
                        room = Room.objects.get(id=room_id)
                        relay.room = room
                        relay.save()
                    except Room.DoesNotExist:
                        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

                return Response({"message": serializer.data})

            # POST method
            elif request.method == "POST":
                # relay.reset()
                if relay.user != request.user:
                    return Response({"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = AddDeviceSerializer(
                    data=request.data,
                    context={"device_id": device_id, "devices": relay.id}
                )
                if serializer.is_valid():
                    room_id = request.data.get("room_id")
                    port = int(request.data.get("port"))  # مطمئن شو این int هست
                    device_fk_id = request.data.get("device")
                    name = request.data.get("name")
                    try:
                        room = Room.objects.get(id=room_id)
                        device_fk = Device.objects.get(id=device_fk_id)
                    except Room.DoesNotExist:
                        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
                    except Device.DoesNotExist:
                        return Response({"message": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

                    # ست کردن فیلد مربوطه از نوع device_r{port} و name{port}
                    setattr(relay, f'device_r{port}', device_fk)
                    setattr(relay, f'name{port}', name)
                    relay.room = room
                    relay.save()

                    if relay_type == "r6":
                        RoomDevice.objects.create(room=room, relay_6=relay, port=port)
                    else:
                        RoomDevice.objects.create(room=room, relay_8=relay, port=port)

                    return Response({"message": serializer.data})

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeviceViewSet(APIView):
    def get(
            self,
            request,
    ):
        r10_devices = Relay10.objects.filter(user=request.user)
        r6_devices = Relay6.objects.filter(user=request.user)
        r10_serializer = Relay10Details(r10_devices, many=True)
        r6_serializer = Relay6Details(r6_devices, many=True)
        return Response({"r12": r10_serializer.data, "r6": r6_serializer.data})


class KeyDevice(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class PsychrometerImageView(ListAPIView):
    queryset = PsychrometerImage.objects.all()
    serializer_class = PsychrometerImageSerializer


# @api_view(("GET",))
# def get_all_device_active_by_relay10_id(request, relay10_id):
#     devices = get_object_or_404(Relay10, pk=relay10_id)
#
#     return Response(serializer.data)

@api_view(["POST", ])
def add_psychrometer_to_relay6(request, relay6_id):
    try:
        with transaction.atomic():
            # ابتدا تلاش می‌کنیم تا رله را پیدا کنیم
            relay6 = Relay6.objects.get(id=relay6_id)

            # بررسی اینکه درخواست به‌صورت POST یا PATCH است
            if request.method == "POST":
                # استفاده از سریالایزر برای پردازش داده‌ها
                serializer = AddPsychrometerToRelay6Serializer(data=request.data, context={"relay6_id": relay6_id})

                if serializer.is_valid():
                    # ذخیره‌سازی داده‌ها
                    serializer.save()

                    return Response({"message": "Psychrometer added successfully", "data": serializer.data},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    except Relay6.DoesNotExist:
        return Response({"message": "Relay6 not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePsychrometerAPIView(APIView):
    def patch(self, request, relay6_id, port):
        if port < 1 or port > 6:
            return Response({"error": "Invalid port number. Must be between 1 and 6."},
                            status=status.HTTP_400_BAD_REQUEST)

        relay = get_object_or_404(Relay6, id=relay6_id)
        psychrometer = getattr(relay, f"t{port}", None)

        if psychrometer is None:
            return Response({"error": "No psychrometer found on this port."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PsychrometerSerializer(psychrometer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, relay6_id, port):
        if port < 1 or port > 6:
            return Response({"error": "Invalid port number. Must be between 1 and 6."},
                            status=status.HTTP_400_BAD_REQUEST)

        relay = get_object_or_404(Relay6, id=relay6_id)
        psychrometer = getattr(relay, f"t{port}", None)

        if not psychrometer:
            return Response({"error": "No psychrometer connected to this port."}, status=status.HTTP_404_NOT_FOUND)

        # پاک‌کردن ارتباط با RoomDevice‌ها
        RoomDevice.objects.filter(psychrometer=psychrometer).delete()

        # پاک‌کردن ارتباط از Relay
        setattr(relay, f"t{port}", None)
        relay.save()

        # حذف خود Psychrometer
        psychrometer.delete()

        return Response({"message": f"Psychrometer on port {port} deleted along with related RoomDevice(s)."},
                        status=status.HTTP_204_NO_CONTENT)
