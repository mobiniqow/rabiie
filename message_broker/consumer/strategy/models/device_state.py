
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

from device.models import Relay10
import time

logging.basicConfig(
    filename="tmp.log",
    format="%(levelname)s %(asctime)s :: %(message)s",
    level=logging.DEBUG,
)


class DeviceStateStrategy(MessageStrategy):
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
                logging.debug("find device by id ", device_id)
                print(f"payload {payload}")
                logging.warning("update jadid hastesh")
                payload = payload
                print(f"papayload {payload}\n")
                for i in range(relay_size):
                    bin2bool = lambda x: bool(int(x))
                    setattr(device, f"r{i + 1}", bin2bool(payload[i]))

                device.updated_at = timezone.now()
                device.save()
                Relay10.objects.filter(pk=device.id).update(updated_at=timezone.now())
            else:
                new_payload = device.get_payload()
                # datime = device.get_time()
                print(f"new_payload[-Message.TOLE_ZAMAN:]{new_payload}")
                message = Message(
                    payload=new_payload,
                    _type="WR",
                    device_id=device_id,
                    # _datetime=datime,
                )
                import time
                time.sleep(0.5)
                self.output(message)
            # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "RR"
