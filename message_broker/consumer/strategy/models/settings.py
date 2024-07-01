import logging
import os


import django
django.setup()

from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message

from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN

from device.models import Relay10
logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)


class SettingsStrategy(MessageStrategy):
    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)

        if _type == RELAY_SIX:
            logging.debug("this is relay10")
            # todo fix relay 6 jobs
            pass
        elif _type == RELAY_TEN:
            device: Relay10 = device
            payload = message.get_body()
            if len(payload) > 0:
                time = message.get_time()
                print(f'message.get_time() {time}')
                logging.debug("find device by id ", device_id)
                if device.updated_at <= time:
                    print(f'payload {payload}')
                    logging.warning("update jadid hastesh")
                    payload = payload
                    print(f'papayload {payload}\n')
                    for i in range(relay_size):
                        bin2bool = lambda x: bool(int(x))
                        setattr(device, f"r{i + 1}", bin2bool(payload[i]))
                        device.save()
                    device.updated_at = time
                    device.save()
                    Relay10.objects.filter(pk=device.id).update(updated_at=time)
            new_payload = device.get_payload()
            datime = device.get_time()
            print(f"new_payload[-Message.TOLE_ZAMAN:]{new_payload}")
            message = Message(payload=new_payload, _type=self.get_code(), device_id=device_id,
                              _datetime=datime)
            self.output(message)
                # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "CD"
