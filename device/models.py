from django.db import models
import uuid
import requests
from authenticate.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from message_warehouse.models import MessageWareHouse


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
    schedular = models.BooleanField(default=False)

    def reset(self):
        bool_fields = [field.name for field in self._meta.get_fields() if isinstance(field, models.BooleanField)]
        for field_name in bool_fields:
            setattr(self, field_name, False)

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

    device_r1 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r1')
    device_r2 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r2')
    device_r3 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r3')
    device_r4 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r4')
    device_r5 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r5')
    device_r6 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r6')
    device_r7 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r7')
    device_r8 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r8')
    device_r9 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay10_device_r9')
    device_r10 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay10_device_r10')
    device_r11 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay10_device_r11')
    device_r12 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay10_device_r12')

    def get_status(self):
        payload = (
            f'r1={self.r1}\r\n'
            f'r2={self.r2}\r\n'
            f'r3={self.r3}\r\n'
            f'r4={self.r4}\r\n'
            f'r5={self.r5}\r\n'
            f'r6={self.r6}\r\n'
            f'r7={self.r7}\r\n'
            f'r8={self.r8}\r\n'
            f'r9={self.r9}\r\n'
            f'r10={self.r10}\r\n'
            f'schedular={1 if self.schedular else 0}\r\n'
        )
        return payload


@receiver(post_save, sender=Relay10)
def relay10_saved(sender, instance, created, **kwargs):
    # todo instance.get_status ro bayad be client befrestonam
    MessageWareHouse(
        relay10_id=instance.id,
        message=instance.get_status(),
        client=instance.product_id
    ).save()
