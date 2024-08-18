from rest_framework import viewsets

from timer.models import DeviceTimer
from timer.serializer import DeviceTimerSerializer


class DeviceTimerView(viewsets.ModelViewSet):
    serializer_class = DeviceTimerSerializer
    def get_queryset(self):
        return DeviceTimer.objects.filter(user=self.request.user)
