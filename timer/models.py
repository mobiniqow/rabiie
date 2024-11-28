from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from authenticate.models import User


def day_validator(value):
    if len(value) != 7:
        raise ValidationError("تعداد روزها درست نیست")
    for i in range(7):
        if value[i] not in ["1", "0"]:
            raise ValidationError("روز ها باید انتخاب شده باشه یا نه")


class DeviceTimer(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    relay10 = models.ForeignKey(
        "device.Relay10", on_delete=models.SET_NULL, blank=True, null=True
    )
    relay6 = models.ForeignKey(
        "device.Relay6", on_delete=models.SET_NULL, blank=True, null=True
    )
    relay_port_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    start_time = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    end_time = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    days = models.CharField(
        max_length=7,
        validators=[
            day_validator,
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def hex_to_binary(hex_string):
        return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    @staticmethod
    def day_timer(binary_schedule):
        timers = []
        start_time = None
        for i, bit in enumerate(binary_schedule):
            if bit == '1':
                if start_time is None:
                    start_time = i + 1
            elif bit == '0' and start_time is not None:
                end_time = i
                timers.append((start_time, end_time))
                start_time = None
        if start_time is not None:
            timers.append((start_time, 24))
        return timers

    @staticmethod
    def parse_schedule(schedule_string):
        relay_number = schedule_string[:2]
        binary_schedule = []
        for i in range(2, len(schedule_string), 6):
            hex_chunk = schedule_string[i:i + 6]
            binary_schedule.append(DeviceTimer.day_timer(DeviceTimer.hex_to_binary(hex_chunk)))
        items = DeviceTimer.get_time_and_date(binary_schedule)
        dates = []
        for item in items:
            item = item.split("=")
            date = item[1]
            times = item[0].split(",")
            start_time = times[0]
            end_time = times[1]
            dt = DeviceTimer()
            dt.relay10 = relay_number
            dt.is_active = True
            dt.start_time = start_time
            dt.end_time = end_time
            dt.days = date
            dates.append(dt)
        return dates

    @staticmethod
    def get_time_and_date(data):
        result_set = set(item for sublist in data for item in sublist)
        items = ""
        for i in result_set:
            tmp = ""
            for index in data:
                tmp += "1" if i in index else "0"
            items += f"{i[0]},{i[1]}={tmp}"
            tmp = ""
        return items

    def clean(self):
        if self.relay10 and self.relay6:
            raise ValidationError("Only one of relay10 or relay6 can be active.")
        elif not self.relay10 and not self.relay6:
            raise ValidationError("Either relay10 or relay6 must be active.")
