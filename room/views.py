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
            "device_ids":device_ids
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
