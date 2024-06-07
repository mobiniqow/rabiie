import logging
import os

os.environ['DJANGO_SETTINGS_MODULE']="core.settings.dev"
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from message_broker.utils.data_type import hex_to_binary
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


class LastStateStrategy(MessageStrategy):
    def input(self, message: Message):
        print("beldele")
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)

        if _type == RELAY_SIX:
            logging.debug("this is relay10")
            # todo fix relay 6 jobs
            pass
        elif _type == RELAY_TEN:
            device: Relay10 = device
            new_payload = device.get_payload()
            datime = device.get_time()
            message = Message(payload=new_payload, _type=self.get_code(), device_id=device_id,
                              _datetime=datime)
            self.output(message)
                # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "DD"
