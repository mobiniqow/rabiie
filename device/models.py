import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authenticate.models import User
from message_broker.message.message import Message
from message_broker.producer.messager import send_broker_message
from message_warehouse.models import MessageWareHouse
from timer.models import DeviceTimer


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=23)
    image = models.ImageField(upload_to="device/image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Psychrometer(models.Model):
    class Mode(models.IntegerChoices):
        THERMOMETER = 1
        HUMIDITY = 2

    mod = models.IntegerField(choices=Mode.choices)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=23)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BaseRelay(models.Model):
    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2
        BLOCK = 3
        FREE = 4

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    client_id = models.CharField(max_length=55, blank=True, null=True)
    state = models.IntegerField(choices=State.choices, default=State.FREE)
    # device_id len
    device_id = models.CharField(max_length=11, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def reset(self):
        bool_fields = [
            field.name
            for field in self._meta.get_fields()
            if isinstance(field, models.BooleanField)
        ]
        for field_name in bool_fields:
            setattr(self, field_name, False)

        fk_fields = [
            field.name
            for field in self._meta.get_fields()
            if isinstance(field, models.ForeignKey)
            and field.name.startswith("device_r")
        ]
        for field_name in fk_fields:
            setattr(self, field_name, None)

    class Meta:
        abstract = True


class Relay6(BaseRelay):
    t1 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t1",
    )
    t2 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t2",
    )
    t3 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t3",
    )
    t4 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t4",
    )
    t5 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t5",
    )
    t6 = models.ForeignKey(
        Psychrometer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="t6",
    )

    r1 = models.BooleanField()
    r2 = models.BooleanField()
    r3 = models.BooleanField()
    r4 = models.BooleanField()
    r5 = models.BooleanField()
    r6 = models.BooleanField()

    device_r1 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r1",
    )
    device_r2 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r2",
    )
    device_r3 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r3",
    )
    device_r4 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r4",
    )
    device_r5 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r5",
    )
    device_r6 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay6_device_r6",
    )


class Relay10(BaseRelay):
    r1 = models.BooleanField()
    r2 = models.BooleanField()
    r3 = models.BooleanField()
    r4 = models.BooleanField()
    r5 = models.BooleanField()
    r6 = models.BooleanField()
    r7 = models.BooleanField()
    r8 = models.BooleanField()
    r9 = models.BooleanField()
    r10 = models.BooleanField()

    name1 = models.CharField(max_length=39, null=True, blank=True)
    name2 = models.CharField(max_length=39, null=True, blank=True)
    name3 = models.CharField(max_length=39, null=True, blank=True)
    name4 = models.CharField(max_length=39, null=True, blank=True)
    name5 = models.CharField(max_length=39, null=True, blank=True)
    name6 = models.CharField(max_length=39, null=True, blank=True)
    name7 = models.CharField(max_length=39, null=True, blank=True)
    name8 = models.CharField(max_length=39, null=True, blank=True)
    name9 = models.CharField(max_length=39, null=True, blank=True)
    name10 = models.CharField(max_length=39, null=True, blank=True)

    device_r1 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r1",
    )
    device_r2 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r2",
    )
    device_r3 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r3",
    )
    device_r4 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r4",
    )
    device_r5 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r5",
    )
    device_r6 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r6",
    )
    device_r7 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r7",
    )
    device_r8 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r8",
    )
    device_r9 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r9",
    )
    device_r10 = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relay10_device_r10",
    )

    def get_payload(self):
        payload = (
            f"{1 if self.r1 else 0}"
            f"{1 if self.r2 else 0}"
            f"{1 if self.r3 else 0}"
            f"{1 if self.r4 else 0}"
            f"{1 if self.r5 else 0}"
            f"{1 if self.r6 else 0}"
            f"{1 if self.r7 else 0}"
            f"{1 if self.r8 else 0}"
            f"{1 if self.r9 else 0}"
            f"{1 if self.r10 else 0}"
        )
        return payload

    def get_time(self):
        time = f'{self.updated_at.strftime("%Y:%m:%d:%H:%M:%S")}'
        return time

    # def get_status(self):
    #     payload = (
    #         f"{1 if self.r1 else 0}"
    #         f"{1 if self.r2 else 0}"
    #         f"{1 if self.r3 else 0}"
    #         f"{1 if self.r4 else 0}"
    #         f"{1 if self.r5 else 0}"
    #         f"{1 if self.r6 else 0}"
    #         f"{1 if self.r7 else 0}"
    #         f"{1 if self.r8 else 0}"
    #         f"{1 if self.r9 else 0}"
    #         f"{1 if self.r10 else 0}"
    #     )
    #     time = f'{self.updated_at.strftime("%Y:%m:%d:%H:%M:%S")}'
    #     print(f"time{time}")
    #     payload_hex = binary_to_hex(payload)
    #     time_hex = string_to_hex(time)
    #
    #     return payload + time

    def get_active_device_by_state_and_name(self):
        return [
            {
                "device": getattr(self, f"device_r{i}"),
                "name": getattr(self, f"name{i}"),
                "state": getattr(self, f"r{i}"),
            }
            for i in range(1, 11)
            if getattr(self, f"device_r{i}")
        ]
        # return [getattr(self, f'device_r{i}') for i in range(1, 11) if getattr(self, f'r{i}')]

    def _time_to_binary(self, start, end):
        day = 24
        result = ""
        for i in range(day):
            if start <= i + 1 <= end:
                result += "1"
            else:
                result += "0"
        return result

    def get_schedular_date(self, relay_number):
        device_timer = DeviceTimer.objects.filter(
            relay10=self,
            is_active=True,
            relay_port_number=relay_number,
        )
        if device_timer.exists():
            device_timer: DeviceTimer = device_timer.first()
            result = self._time_to_binary(
                device_timer.start_time, device_timer.end_time
            )
            result = f"{relay_number:02}{device_timer.days}{result}"

        else:

            # in hex baraye yek roze kamele 24 saateshe
            result = "0000000000000000000000000000000"
            # relay_number = hex(relay_number)[2:].zfill(2)
            result = f"{relay_number:02}{result}"

        return result


@receiver(post_save, sender=Relay10)
def relay10_saved(sender, instance, created, **kwargs):
    # todo instance.get_status ro bayad be client befrestonam
    # todo message ro dorost konam

    #  cd code type settings strategy hastesh majbor shaomda savesh konam
    message = Message(
        payload=instance.get_payload(), _type="CD", device_id=sender.device_id
    )
    send_broker_message(message=message)
    MessageWareHouse(
        relay10=instance,
        message=instance.get_payload(),
    ).save()
