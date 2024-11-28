import logging
import os


from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from django.utils.timezone import now
from .strategy_abs import MessageStrategy

logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)

import time
class ServerTimeStrategy(MessageStrategy):
    def input(self, message: Message):
        _datetime = now()
        message = Message(
            payload=_datetime.strftime("%m:%d:%y:%H:%M:%S"),
            _type=self.get_code(),
            device_id=message.device_id,
            _datetime=_datetime.strftime("%m:%d:%y:%H:%M:%S"),
        )
        time.sleep(0.3)
        self.output(message)
        # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "ST"
