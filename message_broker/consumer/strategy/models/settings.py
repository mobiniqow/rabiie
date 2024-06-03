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


class SettingsStrategy(MessageStrategy):
    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)
        time = message.get_time()
        if _type == RELAY_SIX:
            logging.debug("this is relay10")
            # todo fix relay 6 jobs
            pass
        elif _type == RELAY_TEN:
            device: Relay10 = device
            if device.updated_at < time:
                logging.debug("find device by id ", device_id)
                payload = message.get_body()
                binary_payload = hex_to_binary(payload, relay_size)
                for i in range(relay_size):
                    bin2bool = lambda x: bool(int(x))
                    setattr(device, f"r{i + 1}", bin2bool(binary_payload[i]))
                    device.save()

            else:
                logging.warning("update ghadimi hastesh")
                new_payload = device.get_status()
                message = Message(payload=new_payload, _type=_type, device_id=device_id)
                self.output(message)
                # bayad be hamin device akharin tanzimat ro ersal konim

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "CD"
