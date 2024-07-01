import logging
import os


from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
import django

django.setup()
from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN

from device.models import Relay10

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
        if _type == RELAY_SIX:
            logging.debug("this is relay10")
            # todo fix relay 6 jobs
            pass
        elif _type == RELAY_TEN:
            device: Relay10 = device
            is_online = len(message.payload) > 0
            device.is_online = is_online
            print("Device %s %s %S", device_id, "state", is_online)
            device.save()
            # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "VV"
