from django.contrib import admin
from .models import Relay6, Relay10, Device, Psychrometer


class Relay6Admin(admin.ModelAdmin):
    list_display = [
        "id",
        # 'relay_name',
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
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


admin.site.register(Relay6, Relay6Admin)
admin.site.register(Relay10, Relay10Admin)
admin.site.register(Device)
admin.site.register(Psychrometer)
