from django.shortcuts import get_object_or_404

from user_relations.models import UserChild
from .models import DeviceFactory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserRelayDevice, UserDevice
from .serializers import UserDeviceSerializer


class UserDeviceView(APIView):
    def post(self, request, device_factory_id):
        device_factory = get_object_or_404(DeviceFactory, pk=device_factory_id)
        user = request.user  # Replace this line with your authentication mechanism
        user_device = UserDevice.objects.create(device=device_factory, user=user)
        serializer = UserDeviceSerializer(user_device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_device_id):
        user_device = get_object_or_404(UserDevice, pk=user_device_id)
        user_device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        user = request.user  # Replace this line with your authentication mechanism
        user_devices = UserDevice.objects.filter(user=user)
        serializer = UserDeviceSerializer(user_devices, many=True)
        return Response(serializer.data)


class UserRelayDeviceView(APIView):

    def get(self, request):
        user = request.user  # Replace this line with your authentication mechanism
        user_relay_devices = UserRelayDevice.objects.filter(user=user)
        user_devices = UserDevice.objects.filter(relay__in=user_relay_devices)
        serializer = UserDeviceSerializer(user_devices, many=True)
        return Response(serializer.data)

    def post(self, request, user_device_id, user_relay_device_id):
        user_device = UserDevice.objects.get(pk=user_device_id)
        user_relay_device = UserRelayDevice.objects.get(pk=user_relay_device_id)
        user_relay_device.device.add(user_device)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_device_id, user_relay_device_id):
        user_device = UserDevice.objects.get(pk=user_device_id)
        user_relay_device = UserRelayDevice.objects.get(pk=user_relay_device_id)
        user_relay_device.device.remove(user_device)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        user = request.user  # Replace this line with your authentication mechanism
        user_relay_devices = UserRelayDevice.objects.filter(user=user)
        active_child_users = UserChild.objects.filter(parent=user, state=UserChild.State.ACTIVE)
        active_child_devices = UserDevice.objects.filter(user__in=active_child_users, relay__in=user_relay_devices)
        serializer = UserDeviceSerializer(active_child_devices, many=True)
        return Response(serializer.data)
