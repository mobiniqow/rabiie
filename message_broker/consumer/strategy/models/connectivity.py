import logging
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

django.setup()
from django.utils import timezone
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN

from django.utils.timezone import now
import time
from device.models import Relay10, Relay6

logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)


class ConnectivityStrategy(MessageStrategy):
    """
    agar 1 to pay load bod onnline hastesh
    agar 0 bod offline hastesh
    """

    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)
        print(f"{device} {device} {_type}")
        if _type == RELAY_SIX:
            device: Relay6 = device
            is_online = len(message.payload) > 0
            device.is_online = is_online
            print("Device %s %s %S", device_id, "state", is_online)
            device.save()
            _datetime = now()
            payload = _datetime.strftime("%m/%d/%y:%H:%M:%S")
            message = Message(
                payload=payload,
                _type="WT",
                device_id=device_id,
                _datetime=_datetime.strftime("%m/%d/%y:%H:%M:%S"),
            )
            time.sleep(0.3)
            self.output(message)

        elif _type == RELAY_TEN:
            device: Relay10 = device
            is_online = len(message.payload) > 0
            device.is_online = is_online
            print("Device %s %s %S", device_id, "state", is_online)
            device.save()
            _datetime = timezone.now().astimezone(timezone.get_current_timezone())
            payload = _datetime.strftime("%m/%d/%y:%H:%M:%S")
            message = Message(
                payload=payload,
                _type="WT",
                device_id=device_id,
                _datetime=_datetime.strftime("%m/%d/%y:%H:%M:%S"),
            )
            time.sleep(0.3)
            self.output(message)

            for relay_number in range(1, 11):
                payload = device.get_schedular_date(relay_number)
                message = Message(
                    payload=payload,
                    _type="WS",
                    device_id=device_id,
                    _datetime="",
                )

                self.output(message)
            time.sleep(0.73)
            # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "RG"
