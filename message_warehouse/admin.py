from django.contrib import admin
from .models import MessageWareHouse


@admin.register(MessageWareHouse)
class MessageWareHouseAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "state")
