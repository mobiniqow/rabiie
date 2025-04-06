from django.contrib import admin
from .models import RoomPicture, Room, RoomDevice

@admin.register(RoomPicture)
class RoomPictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'created_at', 'updated_at']
    search_fields = ['id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'image', 'created_at', 'updated_at']
    search_fields = ['name', 'user__user_name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RoomDevice)
class RoomDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'created_at', 'updated_at']
    list_filter = ['room']
    readonly_fields = ['created_at', 'updated_at']
