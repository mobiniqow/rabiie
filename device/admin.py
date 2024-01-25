from django.contrib import admin
from .models import Relay12, Relay6


@admin.register(Relay6)
class Relay6Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'state',
        'product_id',
        'user',
    )


@admin.register(Relay12)
class Relay12Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'state',
        'product_id',
        'user',
    )
