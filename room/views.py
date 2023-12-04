from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, RoomDevice
from .serializers import RoomSerializer, RoomDeviceSerializer


class RoomView(APIView):
    def get(self, request):
        user = request.user  # جایگزین کردن این خط با مکانیزم احراز هویت خودتان
        rooms = Room.objects.filter(user=user)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # جایگزین کردن این خط با مکانیزم احراز هویت خودتان
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDeviceView(APIView):
    def get(self, request):
        user = request.user  # جایگزین کردن این خط با مکانیزم احراز هویت خودتان
        rooms = Room.objects.filter(user=user)
        devices = RoomDevice.objects.filter(room__in=rooms)
        serializer = RoomDeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
