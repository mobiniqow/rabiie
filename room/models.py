from django.db import models
from authenticate.models import User


class RoomPicture(models.Model):
    image = models.ImageField(
        upload_to="rooms",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=54)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ForeignKey(
        RoomPicture, on_delete=models.SET_NULL, null=True, blank=True
    )


class RoomDevice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    # device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True)


#
