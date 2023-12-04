from django.db import models
from device.models import BaseModel
from user_device.models import UserDevice


class EVENT(BaseModel):
    message = models.CharField(max_length=100)
    address = models.CharField(max_length=25)
    input_output = models.BooleanField()
    ack = models.BooleanField(default=False)
    user_device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True)
