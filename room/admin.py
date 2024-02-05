from django.contrib import admin
from room.models import Room, RoomPicture


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomPicture)
class RoomPictureAdmin(admin.ModelAdmin):
    pass
