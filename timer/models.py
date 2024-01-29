from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from authenticate.models import User
from device.models import BaseRelay
from django.core.exceptions import ValidationError


def day_validator(value):
    if len(value) != 7:
        raise ValidationError("تعداد روزها درست نیست")
    for i in range(7):
        if '0' not in value[i] or '1' not in value[i]:
            raise ValidationError("روز ها باید انتخاب شده باشه یا نه")


# شنبه تا جمعه
class DeviceTimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    relay = models.ForeignKey(BaseRelay, on_delete=models.SET_NULL, blank=True, null=True)
    relay_port_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    start_time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    end_time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    days = models.CharField(max_length=7, validators=[day_validator, ])
