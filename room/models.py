from django.db import models
from authenticate.models import User


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=54)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class RoomDevice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    # device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True)
#