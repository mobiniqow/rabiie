from django.contrib import admin
from .models import Relay6, Relay12, Device, Psychrometer


class Relay6Admin(admin.ModelAdmin):
    list_display = [
        'id',
        # 'relay_name',
        'state',
        'product_id',
        'user',
    ]
    list_filter = [
        'state',
        'product_id',
    ]
    search_fields = [
        'relay_name',
        'product_id',
    ]
    list_editable = [
        'state',
    ]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


class Relay12Admin(admin.ModelAdmin):
    list_display = [
        'id',
        'state',
        'product_id',
        'user',
    ]
    list_filter = [
        'state',
        'product_id',
    ]
    search_fields = [
        'product_id',
    ]
    list_editable = [
        'state',
    ]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


admin.site.register(Relay6, Relay6Admin)
admin.site.register(Relay12, Relay12Admin)
admin.site.register(Device)
admin.site.register(Psychrometer)
