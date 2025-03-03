from django.contrib import admin

from .models import Relay6, Relay10, Device, Psychrometer
from django.utils import timezone
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from datetime import date
class Relay6Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "state",
        "device_id",
        "user",
    ]
    list_filter = [
        "state",
        "device_id",
    ]
    search_fields = [
        "relay_name",
        "device_id",
    ]
    readonly_fields = [
        "updated_at",
        "created_at",
    ]
    list_editable = [
        "state",
    ]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


class Relay10Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "state",
        "device_id",
        "user",
    ]
    list_filter = [
        "state",
        "device_id",
    ]
    search_fields = [
        "device_id",
    ]
    list_editable = [
        "state",
    ]
    readonly_fields = [
        "updated_at",
        "created_at",
    ]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    def save_model(self, request, obj, form, change):
        # به روز رسانی دستی updated_at
        obj.updated_at = timezone.now()  # زمان فعلی را به روز رسانی می‌کنیم

        # ارسال پیام برای بروکر
        message = Message(
            payload=obj.get_payload(),
            _type="WR",
            device_id=obj.device_id,
            _datetime=obj.updated_at.strftime("%m/%d/%y:%H:%M:%S")  # فرمت صحیح تاریخ و زمان
        )
        send_broker_message(message=message)

        # ذخیره مدل
        super().save_model(request, obj, form, change)
admin.site.register(Relay6, Relay6Admin)
admin.site.register(Relay10, Relay10Admin)
admin.site.register(Device)
admin.site.register(Psychrometer)
