from django.db import models
from authenticate.models import User
from device.models import BaseModel
from user_device.models import UserDevice


class Room(BaseModel):
    name = models.CharField(max_length=54)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class RoomDevice(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True)
