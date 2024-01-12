from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from authenticate.models import User
from device.models import DeviceFactory, BaseModel


class UserDevice(BaseModel):
    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2
        BANNED = 3
        REPORTED = 4

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    device = models.ForeignKey(DeviceFactory, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField()
    current_state = models.JSONField()
    des_state = models.JSONField()
    ip_address = models.CharField(max_length=25, blank=True)


class UserRelayDevice(BaseModel):
    relay = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True, related_name='user_relay')
    device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True, related_name='user_device')
    port_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])


class DeviceIPHistory(BaseModel):
    device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True, )
    ip_address = models.CharField(max_length=25)
