from logging import raiseExceptions

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from device.models import Relay10, Relay6
from device.serializers import Relay10Details, Relay6Details
from .models import Room, RoomDevice, RoomPicture
from .serializers import RoomSerializer, RoomDeviceSerializer, RoomPictureSerializer


class RoomView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(user=user)


class RoomDeviceListAPIView(APIView):
    def get(self, request, room_id):
        room_devices = RoomDevice.objects.filter(room_id=room_id)
        response_data = []

        for rd in room_devices:
            if rd.device:
                device_id = str(rd.device.id)
                device_info = {
                    "type": "Device",
                    "device_id": device_id,
                    "device_name": rd.device.name,
                    "device_image": rd.device.image.url if rd.device.image else None,
                }

                relay6_ports = [
                    (relay, i)
                    for i in range(1, 7)
                    for relay in Relay6.objects.filter(**{f'device_r{i}': rd.device})
                    if getattr(relay, f'device_r{i}') == rd.device
                ]

                relay10_ports = [
                    (relay, i)
                    for i in range(1, 11)
                    for relay in Relay10.objects.filter(**{f'device_r{i}': rd.device})
                    if getattr(relay, f'device_r{i}') == rd.device
                ]

                for relay, port in relay6_ports:
                    response_data.append({
                        **device_info,
                        "connected_to": "Relay6",
                        "relay_id": str(relay.id),
                        "port_number": port,
                        "port_name": getattr(relay, f'name{port}', ''),
                        "relay_state": getattr(relay, f'r{port}'),
                    })

                for relay, port in relay10_ports:
                    response_data.append({
                        **device_info,
                        "connected_to": "Relay10",
                        "relay_id": str(relay.id),
                        "port_number": port,
                        "port_name": getattr(relay, f'name{port}', ''),
                        "relay_state": getattr(relay, f'r{port}'),
                    })

            elif rd.psychrometer:
                psychrometer_id = str(rd.psychrometer.id)
                psychrometer_info = {
                    "type": "Psychrometer",
                    "psychrometer_id": psychrometer_id,
                    "psychrometer_name": rd.psychrometer.name,
                    "psychrometer_image": (
                        rd.psychrometer.image.image.url
                        if rd.psychrometer.image and rd.psychrometer.image.image
                        else None
                    ),
                    "mode": rd.psychrometer.get_mod_display(),
                    "current_value": rd.psychrometer.current_value,
                    "destination_value": rd.psychrometer.destination_value,
                    "tolerance": rd.psychrometer.tolerance,
                }

                relay6_ports = [
                    (relay, i)
                    for i in range(1, 7)
                    for relay in Relay6.objects.filter(**{f't{i}': rd.psychrometer})
                    if getattr(relay, f't{i}') == rd.psychrometer
                ]

                for relay, port in relay6_ports:
                    response_data.append({
                        **psychrometer_info,
                        "connected_to": "Relay6",
                        "relay_id": str(relay.id),
                        "port_number": port,
                        "port_name": getattr(relay, f'name{port}', ''),
                        "relay_state": getattr(relay, f'r{port}'),
                    })

        return Response(response_data, status=status.HTTP_200_OK)


class RoomDeviceView(APIView):
    def get(self, request, room_id):
        user = request.user
        room_devices = RoomDevice.objects.filter(room__user=user, room_id=room_id)
        device_serializer = RoomDeviceSerializer(room_devices, many=True)
        device_ids = list(room_devices.values_list('device_id', flat=True))
        psychrometer_ids = list(room_devices.values_list('psychrometer', flat=True))
        device_ids += [pid for pid in psychrometer_ids if pid is not None]
        relay10_q = Q()
        for i in range(1, 11):
            relay10_q |= Q(**{f"device_r{i}__in": device_ids})
        relay6_q = Q()
        for i in range(1, 7):
            relay6_q |= Q(**{f"device_r{i}__in": device_ids})
            relay6_q |= Q(**{f"t{i}__in": device_ids})
        r10_devices = Relay10.objects.filter(user=user).filter(relay10_q)
        r6_devices = Relay6.objects.filter(user=user).filter(relay6_q)
        r10_serializer = Relay10Details(r10_devices, many=True)
        r6_serializer = Relay6Details(r6_devices, many=True)
        return Response({
            "room_devices": device_serializer.data,
            "relay10": r10_serializer.data,
            "relay6": r6_serializer.data,
            "device_ids": device_ids
        })

    def post(self, request, room_id):

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "اتاق مورد نظر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomDeviceSerializer(data=request.data)
        if serializer.is_valid(raiseExceptions=True):
            serializer.save(room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomPictureList(ListAPIView):
    serializer_class = RoomPictureSerializer
    queryset = RoomPicture.objects.all()
