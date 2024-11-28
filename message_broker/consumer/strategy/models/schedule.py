import logging

import django
from django.db import transaction

from timer.models import DeviceTimer

django.setup()
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
            if message.payload == "":
                for relay_number in range(1, 11):
                    payload = device.get_schedular_date(relay_number)
                    datime = device.get_time()
                    message = Message(
                        payload=payload,
                        _type="WS",
                        device_id=device_id,
                        _datetime="",
                    )
                    time.sleep(1)
                    self.output(message)
            #  agar date time khali bod yani in ke timer hasho mikhad set kone
            else :
                if len(message.payload) == 2:
                    relay_number = int(message.payload)
                    print(f"relay_number2 {relay_number}")
                    print(f"message.payload {message.payload}")
                    if relay_number <= relay_size:
                        print(f"relay_number {relay_number}")
                        payload = device.get_schedular_date(relay_number)
                        print(f"relay_number payload {payload}")
                        datime = device.get_time()
                        message = Message(
                            payload=payload,
                            _type=self.get_code(),
                            device_id=device_id,
                            _datetime="",
                        )
                        time.sleep(1)
                        self.output(message)
                else:
                    self.set_time_relay(device,message.payload)
            # elif message.datetime != "":
            #     print(f"message {message.payload}")
            #     relay_number = int(message.payload[:2], 10)
            #     device_timer = DeviceTimer.objects.filter(
            #         relay_port_number=relay_number, relay10__device_id=message.device_id
            #     )
            #     start_time, end_time = self.__get_range_time(message.payload[9:])
            #     days = message.payload[2:9]
            #     if device_timer.exists():
            #         device_timer: DeviceTimer = device_timer.first()
            #         if device_timer.updated_at <= message.get_time():
            #             if start_time == -1:
            #                 device_timer.is_active = False
            #                 device_timer.days = "0000000"
            #                 device.updated_at = message.get_time()
            #                 device.save()
            #
            #             else:
            #                 device_timer.start_time = start_time
            #                 device_timer.end_time = end_time
            #                 device_timer.days = days
            #                 device_timer.updated_at = message.get_time()
            #                 device_timer.save()
            #     elif start_time != -1:
            #         relay = Relay10.objects.get(device_id=message.device_id)
            #         DeviceTimer.objects.create(
            #             relay_port_number=relay_number,
            #             relay10=relay,
            #             start_time=start_time,
            #             end_time=end_time,
            #             days=days,
            #             user=relay.user,
            #             updated_at=message.get_time(),
            #         )
    @transaction.atomic
    def set_time_relay(self, device,payload):
        device_timers = DeviceTimer.parse_schedule( payload)
        DeviceTimer.objects.all().delete()
        for timer in device_timers:
            timer.relay10 = device
            timer.user = device.user
            timer.save()


    def output(self, message: Message):
        send_broker_message(message)

    def get_code(self) -> str:
        return "RS"

    def __hex_to_binary(self, _hex):
        WEEK = 7
        HOUR = 24
        num_of_bits = WEEK * HOUR
        return bin(int(_hex, 16))[2:].zfill(num_of_bits)

    def __get_range_time(self, time_binary):
        """
        conver binary time to tuple start and end

        :param time_binary:
        :return:
        """
        start_time = -1
        end_time = -1
        for index, hour in enumerate(time_binary):
            if hour == "1":
                # agar avalin addad ro did bege starte va shayad hamon saat
                # ham mitone entehashbashe end time hame hamon value mizarim
                if start_time == -1:
                    start_time = index + 1
                    end_time = index + 1
                else:
                    end_time = index + 1
        return start_time, end_time
