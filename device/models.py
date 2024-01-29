from django.db import models
import uuid
import requests
from authenticate.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=23)
    image = models.ImageField(upload_to='device/image')
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
    updated_at = models.DateTimeField(auto_now=True)
    client_id = models.CharField(max_length=55, blank=True, null=True)
    state = models.IntegerField(choices=State.choices, default=State.FREE)
    product_id = models.CharField(max_length=22, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def reset(self):
        # Get all the boolean field names starting with 'r' and set them to False
        bool_fields = [field.name for field in self._meta.get_fields() if isinstance(field, models.BooleanField)]
        for field_name in bool_fields:
            setattr(self, field_name, False)

        # Get all the foreign key field names starting with 'device_r' and set them to None
        fk_fields = [field.name for field in self._meta.get_fields() if isinstance(field, models.ForeignKey)
                     and field.name.startswith('device_r')]
        for field_name in fk_fields:
            setattr(self, field_name, None)

    class Meta:
        abstract = True


class Relay6(BaseRelay):
    t1 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t1')
    t2 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t2')
    t3 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t3')
    t4 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t4')
    t5 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t5')
    t6 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL, related_name='t6')

    r1 = models.BooleanField()
    r2 = models.BooleanField()
    r3 = models.BooleanField()
    r4 = models.BooleanField()
    r5 = models.BooleanField()
    r6 = models.BooleanField()

    device_r1 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r1')
    device_r2 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r2')
    device_r3 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r3')
    device_r4 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r4')
    device_r5 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r5')
    device_r6 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay6_device_r6')


class Relay12(BaseRelay):
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

    device_r1 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r1')
    device_r2 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r2')
    device_r3 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r3')
    device_r4 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r4')
    device_r5 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r5')
    device_r6 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r6')
    device_r7 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r7')
    device_r8 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r8')
    device_r9 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay12_device_r9')
    device_r10 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay12_device_r10')
    device_r11 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay12_device_r11')
    device_r12 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay12_device_r12')


@receiver(post_save, sender=Relay12)
def relay12_saved(sender, instance, created, **kwargs):
    result = [
        instance.r1, instance.r2,
        instance.r3, instance.r4,
        instance.r5, instance.r6,
        instance.r7, instance.r8,
        instance.r9, instance.r10,
    ]

    url = "localhost:8080/"

    payload = 'client_id=127.0.0.1%3A52062&r1=false&r2=false&r3=false&r4=false&r5=false&r6=false&r7=false&r8=true&r9=true'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response)