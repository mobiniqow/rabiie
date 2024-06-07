import logging
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "core.settings.dev"
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from message_broker.utils.data_type import hex_to_binary
from django.utils.timezone import now
from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN

from device.models import Relay10

logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)


class ServerTimeStrategy(MessageStrategy):
    def input(self, message: Message):
        _datetime = now()
        message = Message(payload="", _type=self.get_code(), device_id=message.device_id,
                          _datetime=_datetime.strftime("%Y:%m:%d:%H:%M:%S"))
        self.output(message)
        # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "ST"
