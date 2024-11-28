from django.utils import timezone
from datetime import datetime
import logging
import time

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


class ServerTimeStrategy(MessageStrategy):
    def input(self, message: Message):
        device_id = message.device_id
        device, _type, relay_size = get_device_by_id(device_id=device_id)
        payload = message.get_body()
        _datetime = timezone.now()  # Server's current time

        # If payload is empty, send server time
        if message.payload == "":
            payload = _datetime.strftime("%m/%d/%y:%H:%M:%S")
            message = Message(
                payload=payload,
                _type=self.get_code(),
                device_id=device_id,
                _datetime=_datetime.strftime("%m/%d/%y:%H:%M:%S"),
            )
            time.sleep(0.3)
            self.output(message)
            return

        if _type == RELAY_TEN:
            device: Relay10 = device
            time_from_message = message.payload

            # Convert the time_from_message (string) to a datetime object (naive)
            time_from_message_datetime = datetime.strptime(time_from_message, "%m/%d/%y:%H:%M:%S")

            # Make the naive datetime object aware by using the timezone
            time_from_message_datetime = timezone.make_aware(time_from_message_datetime, timezone.get_current_timezone())

            print(f"device.updated_at: {device.updated_at}")
            print(f"time_from_message_datetime: {time_from_message_datetime}")
            # Compare time_from_message_datetime with device.updated_at
            if device.updated_at is None or device.updated_at >= time_from_message_datetime:
                # If the device's last update time is newer, send the last settings
                print(f"Sending last settings for device {device_id}")
                last_payload = device.get_payload()
                message = Message(
                    payload=last_payload,
                    _type="WR",  # ST code for sending last settings
                    device_id=device_id,
                    _datetime="",
                )

            else:
                print(f"Sending WR (new settings) for device {device_id}")
                logging.warning("Sending new settings with WR code")
                new_payload = self.create_new_payload(device)
                message = Message(
                    payload="",
                    _type="RR",
                    device_id=device_id,
                    _datetime="",
                )
                # taghvim
                message = Message(
                    payload="",
                    _type="RS",
                    device_id=device_id,
                    _datetime="",
                )

            # ارسال پیام
            time.sleep(0.3)
            self.output(message)

    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "ST"

    def create_new_payload(self, device: Relay10) -> str:
        # This function creates a new payload for the device
        return device.get_payload()  # Customize this based on your needs
