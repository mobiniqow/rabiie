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

    hc = models.BooleanField(default=False)
    ma = models.BooleanField(default=False)
    on_of = models.BooleanField(default=False)
    plus_minus = models.BooleanField(default=False)
    current_value = models.IntegerField(default=0)
    destination_value = models.IntegerField(default=0)
    tolerance = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_body(self):
        return (
            f"{int(self.hc)}{int(self.ma)}{int(self.on_of)}{int(self.plus_minus)}"
            f"{self.destination_value:03}{self.tolerance:02}"
        )

    def set_payload(self, payload):
        self.hc = bool(int(payload[0]))
        self.ma = bool(int(payload[1]))
        self.on_of = bool(int(payload[2]))
        self.plus_minus = bool(int(payload[3]))
        self.destination_value = int(payload[4:7])
        self.tolerance = int(payload[7:9])
        self.current_value = int(payload[9:12])
        print(f"payload {payload}")


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
    device_id = models.CharField(max_length=110, db_index=True)
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
    updated_at = models.DateTimeField(auto_now=True)
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
    name1 = models.CharField(max_length=39, null=True, blank=True)
    name2 = models.CharField(max_length=39, null=True, blank=True)
    name3 = models.CharField(max_length=39, null=True, blank=True)
    name4 = models.CharField(max_length=39, null=True, blank=True)
    name5 = models.CharField(max_length=39, null=True, blank=True)
    name6 = models.CharField(max_length=39, null=True, blank=True)

    def get_payload(self, relay=0):
        payload = ""
        if relay == 0:
            for i in range(1, 7):
                payload += getattr(self, f't{i}').get_body()
        else:
            payload = getattr(self, f't{relay}').get_body()
        return payload

    def write_payload(self, relay=0, payload=""):
        print(f"hi my device is  {payload} {relay}")
        if relay != 0:
            temperature = getattr(self, f't{relay}')
            temperature.set_payload(payload)
            temperature.save()
            print(f"hi my device is  {payload}")
            payload = getattr(self, f't{relay}').get_body()
        return payload


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
        if self.updated_at is not None:
            time = f'{self.updated_at.strftime("%m/%d/%y:%H:%M:%S")}'
        else:
            time = f'{self.created_at.strftime("%m/%d/%y:%H:%M:%S")}'
        return time

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

    def binary_to_hex(self, binary_string):
        hex_result = hex(int(binary_string, 2))[2:].upper()  # تبدیل به هگزادسیمال و حذف '0x'
        hex_result = hex_result.zfill(42)
        return hex_result

    def get_schedular_date(self, relay_number):
        device_timers = DeviceTimer.objects.filter(
            is_active=True,
            relay_port_number=relay_number,
        )
        if not device_timers.exists():
            return f"{relay_number:02}000000000000000000000000000000000000000000"
        schedule = [0] * (7 * 24)
        for device_timer in device_timers:
            days = device_timer.days
            for i, day_active in enumerate(days):
                if day_active == '1':
                    for hour in range(device_timer.start_time-1, device_timer.end_time ):
                        index = i * 24 + hour
                        if index < 7 * 24:
                            schedule[index] = 1
        binary_result = ''.join(map(str, schedule))
        print(f'binary_result i {binary_result}')
        binary_result = self.reverse_week(binary_result)
        print(f'reverse_week i {binary_result}')
        hex_result = self.binary_to_hex(binary_result)

        result = f"{relay_number:02}{hex_result}"
        return result

    def reverse_day_binary(self, day_binary):
        return day_binary[::-1]

    def reverse_week(self, week_binary):
        result = ""
        for i in range(7):
            result += self.reverse_day_binary(week_binary[i* 24:((i + 1) * 24)])
        return result
