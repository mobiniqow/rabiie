



from rest_framework import viewsets
from .models import DeviceTimer
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from device.models import Relay10
from .serializer import DeviceTimerSerializer


class DeviceTimerView(viewsets.ModelViewSet):
    serializer_class = DeviceTimerSerializer

    def get_queryset(self):
        return DeviceTimer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        self.send_relay_message(instance)

    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user)
        self.send_relay_message(instance)

    def send_relay_message(self, timer: DeviceTimer):
        relay_number = timer.relay_port_number  # شماره رله‌ای که تایمرش تغییر کرده

        # پیدا کردن رله‌ای که به این دیوایس تعلق داره
        related_relay = Relay10.objects.filter(
            device_id=timer.device.device_id
        ).first()

        if not related_relay:
            return  # رله‌ای پیدا نشد که مربوط به این دیوایس باشه

        # ساخت پیام برای همون رله
        payload = related_relay.get_schedular_date(relay_number)

        message = Message(
            payload=payload,
            _type="RS",
            device_id=related_relay.device_id,
            _datetime=related_relay.get_time(),
        )
        send_broker_message(message)
