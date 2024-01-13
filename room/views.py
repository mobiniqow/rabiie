from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Room, RoomDevice
from .serializers import RoomSerializer, RoomDeviceSerializer


class RoomView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(user=user)


class RoomDeviceView(APIView):
    def get(self, request, room_id):
        user = request.user
        devices = RoomDevice.objects.filter(room__user=user, room_id=room_id)
        serializer = RoomDeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):
        var = {}
        var.update(request.data)
        var['room'] = room_id
        serializer = RoomDeviceSerializer(data=var,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
