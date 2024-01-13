from django.contrib import admin
from .models import *


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyedDevice)
class KeyedDeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceFactory)
class DeviceFactoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Humidity)
class HumidityAdmin(admin.ModelAdmin):
    pass
