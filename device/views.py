from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from django.db import transaction
from device.models import Relay10, Relay6, Device
from device.serializers import (
    Relay10Serializer,
    Relay6Serializer,
    DeviceSerializer,
    Relay10Details,
    AddDeviceSerializer,
    Relay6Details,
)
from room.models import Room


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
            serializer = Relay10Serializer(
                devices.first(), data=request.data, partial=True
            )
        if not devices.exists():
            devices = Relay6.objects.filter(device_id=device_id)
            if devices.exists():
                serializer = Relay6Serializer(
                    devices.first(), data=request.data, partial=True
                )
        if not devices.exists():
            return Response(
                {"message": "object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        message = Message(
            payload=instance.get_payload(), _type="WR", device_id=instance.device_id,_datetime=instance.get_time()
        )

        send_broker_message(message=message)
        return Response({"message": serializer.data})




@api_view(("PATCH", "POST"))
def client_device(request, device_id):
    try:
        with transaction.atomic():
            # بررسی روش درخواست (PATCH یا POST)
            if request.method == "PATCH":
                # ابتدا تلاش می‌کنیم دستگاه را پیدا کنیم
                devices = Relay10.objects.filter(device_id=device_id)
                if devices.exists():
                    serializer = Relay10Serializer(devices.first(), data=request.data, partial=True)
                else:
                    devices = Relay6.objects.filter(device_id=device_id)
                    if devices.exists():
                        serializer = Relay6Serializer(devices.first(), data=request.data, partial=True)

                # اگر دستگاهی پیدا نشد
                if not devices.exists():
                    return Response({"message": "object not found"}, status=status.HTTP_404_NOT_FOUND)

                # بررسی صحت داده‌ها
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # اگر room_id وجود داشته باشد، به روم اضافه کنیم
                room_id = request.data.get("room_id")
                if room_id:
                    try:
                        room = Room.objects.get(id=room_id)
                        device = serializer.instance
                        device.room = room  # ارتباط دادن دستگاه به روم
                        device.save()
                    except Room.DoesNotExist:
                        return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

                return Response({"message": serializer.data})

            elif request.method == "POST":
                # پیدا کردن دستگاه بر اساس device_id
                devices = Relay10.objects.filter(device_id=device_id)
                if devices.exists():
                    relay = devices.first()
                else:
                    devices = Relay6.objects.filter(device_id=device_id)
                    if devices.exists():
                        relay = devices.first()

                # اگر دستگاه پیدا نشد
                if not devices.exists():
                    return Response({
                        "message": len(Relay10.objects.filter(device_id=device_id)),
                        "id": device_id,
                    }, status=status.HTTP_404_NOT_FOUND)

                # ریست کردن دستگاه
                relay.reset()

                # بررسی مالک دستگاه
                if relay.user != request.user:
                    return Response({"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)

                # ایجاد و ذخیره دستگاه جدید
                serializer = AddDeviceSerializer(data=request.data, context={"device_id": device_id})

                # بررسی صحت داده‌ها و ذخیره کردن
                if serializer.is_valid():
                    # قبل از ذخیره دستگاه، بررسی روم و افزودن آن
                    room_id = request.data.get("room_id")
                    if room_id:
                        try:
                            room = Room.objects.get(id=room_id)
                            relay.room = room  # اتصال به روم
                            relay.save()
                        except Room.DoesNotExist:
                            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

                    serializer.save()
                    return Response({"message": serializer.data})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # هر ارور غیرمنتظره‌ای که پیش آمد، همه چیز رو رول بک می‌کنیم
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


# @api_view(("GET",))
# def get_all_device_active_by_relay10_id(request, relay10_id):
#     devices = get_object_or_404(Relay10, pk=relay10_id)
#
#     return Response(serializer.data)
