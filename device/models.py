from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Relay(BaseModel):
    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)

    name = models.CharField(max_length=43)
    number_of_port = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)])


class KeyedDevice(BaseModel):
    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2

    name = models.CharField(max_length=43)
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)


class Temperature(BaseModel):
    name = models.CharField(max_length=33)
    state = models.JSONField()


class Humidity(BaseModel):
    name = models.CharField(max_length=33)
    state = models.JSONField()


class DeviceFactory(BaseModel):
    DEVICE_CHOICES = [
        ('relay', 'Relay'),
        ('keyed_device', 'Keyed Device'),
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
    ]

    name = models.CharField(max_length=50)
    device_type = models.CharField(choices=DEVICE_CHOICES, max_length=20)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
