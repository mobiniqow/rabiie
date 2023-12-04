from rest_framework.generics import ListAPIView

from device.models import KeyedDevice
from device.serializers import KeyedDeviceSerializers


class DeviceListView(ListAPIView):
    serializer_class = KeyedDeviceSerializers
    queryset = KeyedDevice.objects.filter(state=KeyedDevice.State.ACTIVE)
