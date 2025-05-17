import os

import django

os.environ["DJANGO_MODULE_SETTINGS"] = "core.settings.prod"
django.setup()

from device.models import Relay10, Relay6

RELAY_SIX = "RELAY6"
RELAY_TEN = "RELAY10"

def get_device_by_id(device_id):
    relay = Relay6.objects.filter(device_id=device_id)
    print(f'relay {relay} device_id {device_id}')
    if relay.exists():
        return relay.first(), RELAY_SIX, 6
    else:
        relay = Relay10.objects.filter(device_id=device_id)
        if relay.exists():
            return relay.first(), RELAY_TEN, 10
    return None, None, None
