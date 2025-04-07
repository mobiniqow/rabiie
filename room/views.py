from logging import raiseExceptions

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

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

from django.db import models
class RoomDeviceView(APIView):
    def get(self, request, room_id):
        user = request.user

        # 1. RoomDeviceها رو بگیر برای اون اتاق
        room_devices = RoomDevice.objects.filter(room__user=user, room_id=room_id)
        device_serializer = RoomDeviceSerializer(room_devices, many=True)

        # 2. از RoomDevice، id دیوایس‌ها رو بگیر
        device_ids = [i for i in room_devices.values_list('device_id', flat=True)]
        psychrometer_ids = [i for i in room_devices.values_list('psychrometer', flat=True)]
        device_ids = device_ids + psychrometer_ids
        # 3. Relay10 ها رو فیلتر کن که حداقل یکی از device_r1 تا device_r10 داخل device_ids باشه
        r10_devices = Relay10.objects.filter(
            user=user
        ).filter(
            models.Q(device_r1__in=device_ids) |
            models.Q(device_r2__in=device_ids) |
            models.Q(device_r3__in=device_ids) |
            models.Q(device_r4__in=device_ids) |
            models.Q(device_r5__in=device_ids) |
            models.Q(device_r6__in=device_ids) |
            models.Q(device_r7__in=device_ids) |
            models.Q(device_r8__in=device_ids) |
            models.Q(device_r9__in=device_ids) |
            models.Q(device_r10__in=device_ids)
        )

        r6_devices = Relay6.objects.filter(
            user=user
        ).filter(
            models.Q(device_r1__in=device_ids) |
            models.Q(device_r2__in=device_ids) |
            models.Q(device_r3__in=device_ids) |
            models.Q(device_r4__in=device_ids) |
            models.Q(device_r5__in=device_ids) |
            models.Q(device_r6__in=device_ids) |
            models.Q(t1__in=device_ids) |
            models.Q(t2__in=device_ids) |
            models.Q(t3__in=device_ids) |
            models.Q(t4__in=device_ids) |
            models.Q(t5__in=device_ids) |
            models.Q(t6__in=device_ids)
        )

        r10_serializer = Relay10Details(r10_devices, many=True)
        r6_serializer = Relay6Details(r6_devices, many=True)

        return Response({
            # "room_devices": device_serializer.data,
            "relay10": r10_serializer.data,
            "relay6": r6_serializer.data,
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
