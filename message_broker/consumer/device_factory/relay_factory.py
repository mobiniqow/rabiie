import os

import django

os.environ['DJANGO_MODULE_SETTINGS'] = "core.settings.prod"
django.setup()

from device.models import Relay10, Relay6

RELAY_SIX = "RELAY6"
RELAY_TEN = "RELAY10"


def get_device_by_id(device_id):
    relay = Relay6.objects.get(device_id=device_id)
    if relay is not None:
        return relay, RELAY_SIX
    else:
        relay = Relay10.objects.get(device_id=device_id)
        if relay is not None:
            return relay, RELAY_TEN
    return None, None
