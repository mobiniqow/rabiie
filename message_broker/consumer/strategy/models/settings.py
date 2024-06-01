import os

from device.models import Relay10
from .strategy_abs import MessageStrategy
from ...device_factory.relay_factory import get_device_by_id, RELAY_SIX, RELAY_TEN


class Settings(MessageStrategy):

    def do_get(self):
        device_id = self.message.device_id
        device, type = get_device_by_id(device_id=device_id)
        time = self.message.get_time()
        if type == RELAY_SIX:
            print("this is relay10")
            pass
        elif type == RELAY_TEN:
            device:Relay10 = device
            device.r

    def do_set(self):
        pass
