import logging
import os
import time

import django

django.setup()
from django.utils import timezone
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message

from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN

from device.models import Relay6
import time

logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)


class TemperatureStrategy(MessageStrategy):
    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)
        if _type == RELAY_SIX:
            device: Relay6 = device
            payload = message.get_body()
            print(f'sdads {payload} {len(payload)}')
            if len(payload) == 2:
                print("find device by id {device_id}", )
                device_id = message.device_id
                new_payload = device.get_payload(int(payload[:2]))
                # shomare tp + payload
                message = Message(
                    payload=f'{int(payload[:2]):02}{new_payload}',
                    _type="WH",
                    device_id=device_id,
                    _datetime=device.updated_at.strftime("%m/%d/%y:%H:%M:%S")
                )
                import time
                time.sleep(0.5)
                self.output(message)
            elif len(payload) == 0:
                logging.debug("find device by id ", device_id)
                device_id = message.device_id
                new_payload = device.get_payload()
                message = Message(
                    payload=new_payload,
                    _type="WH",
                    device_id=device_id,
                    _datetime=device.updated_at.strftime("%m/%d/%y:%H:%M:%S")
                )
                import time
                time.sleep(0.5)
                self.output(message)
            else:
                print(f"find device bassdy id  {device_id}")
                device_id = message.device_id
                new_payload = device.write_payload(int(payload[:2]), payload[2:])
                # shomare tp + payload
                message = Message(
                    payload=f'{int(payload[:2]):02}{new_payload}',
                    _type="WH",
                    device_id=device_id,
                    _datetime=device.updated_at.strftime("%m/%d/%y:%H:%M:%S")
                )
                import time
                time.sleep(0.5)
                self.output(message)

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "RH"
