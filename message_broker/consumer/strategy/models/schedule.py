import logging
import os

from timer.models import DeviceTimer

os.environ['DJANGO_SETTINGS_MODULE']="core.settings.dev"
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


class ScheduleStrategy(MessageStrategy):
    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)
        if _type == RELAY_SIX:
            logging.debug("this is relay10")
            # todo fix relay 6 jobs
            pass
        elif _type == RELAY_TEN:
            device: Relay10 = device
            DeviceTimer.objects.filter()
            if message.payload == "":
                for relay_number in range(1, 8):
                    payload = device.get_schedular_date(relay_number)
                    datime = device.get_time()
                    message = Message(payload=payload, _type=self.get_code(), device_id=device_id,
                                      _datetime=datime)
                    self.output(message)
            #  agar date time khali bod yani in ke timer hasho mikhad set kone
            elif message.datetime == "":
                relay_number = int(message.payload, 2)
                if relay_number <= relay_size:
                    print(f'relay_number {relay_number}')
                    payload = device.get_schedular_date(relay_number)
                    print(f'relay_number payload {payload}')
                    datime = device.get_time()
                    message = Message(payload=payload, _type=self.get_code(), device_id=device_id,
                                      _datetime=datime)

                    self.output(message)
                elif message.datetime != "":
                    relay_number = int(message.payload[:2], 16)
                    _hex = message.payload[2:]
                    # binary = self.__hex_to_binary(_hex)
                    print()
                    # if relay_number <= relay_size:
                    #     print(f'relay_number {relay_number}')
                    #     payload = device.get_schedular_date(relay_number)
                    #     print(f'relay_number payload {payload}')
                    #     datime = device.get_time()
                    #     message = Message(payload=payload, _type=self.get_code(), device_id=device_id,
                    #                       _datetime=datime)
                    #     self.output(message)

                # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "SD"

    def __hex_to_binary(self, _hex):
        WEEK = 7
        HOUR = 24
        num_of_bits = WEEK * HOUR
        return bin(int(_hex, 16))[2:].zfill(num_of_bits)
