from django.db import models


class MessageWareHouse(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 1
        SUCCESSFULLY = 2
        TRY = 3

    relay6 = models.ForeignKey(
        "device.Relay6",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="relay_6",
    )
    relay10 = models.ForeignKey(
        "device.Relay10",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="relay_10",
    )
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    message = models.CharField(
        max_length=222,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
