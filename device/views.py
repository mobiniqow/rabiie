from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message

from device.models import Relay10, Relay6, Device
from device.serializers import (
    Relay10Serializer,
    Relay6Serializer,
    DeviceSerializer,
    Relay10Details,
    AddDeviceSerializer,
    Relay6Details,
)


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
        serializer.save()
        return Response({"message": serializer.data})

    if request.method == "POST":
        devices = Relay10.objects.filter(device_id=device_id)
        if devices.exists():
            relay = devices.first()
        else:
            devices = Relay6.objects.filter(device_id=device_id)
            if devices.exists():
                relay = devices.first()
        if not devices.exists():
            return Response(
                {
                    "message": len(Relay10.objects.filter(device_id=device_id)),
                    "id": device_id,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        relay.reset()

        if relay.user != request.user:
            return Response(
                {"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AddDeviceSerializer(
            data=request.data, context={"device_id": device_id}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(("GET",))
def get_all_device_active_by_relay10_id(request, relay10_id):
    devices = get_object_or_404(Relay10, pk=relay10_id)

    return Response(serializer.data)
