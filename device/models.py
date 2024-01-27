from django.db import models
import uuid

from authenticate.models import User


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

    mod = models.IntegerField(choices=Mode.choices, )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=23)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Relay6(models.Model):
    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2
        BlOCK = 3
        FREE = 4

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=State.choices, default=State.FREE)
    product_id = models.CharField(max_length=22, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    t1 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
    t2 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
    t3 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
    t4 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
    t5 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
    t6 = models.ForeignKey(Psychrometer, null=True, blank=True, on_delete=models.SET_NULL)
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

    def reset(self):
        self.r1 = False
        self.r2 = False
        self.r3 = False
        self.r4 = False
        self.r5 = False
        self.r6 = False

        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.t5 = None
        self.t6 = None

        self.device_r1 = None
        self.device_r2 = None
        self.device_r3 = None
        self.device_r4 = None
        self.device_r5 = None
        self.device_r6 = None


class Relay12(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class State(models.IntegerChoices):
        ACTIVE = 0
        DE_ACTIVE = 1
        SUSPEND = 2
        BlOCK = 3
        FREE = 4

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=State.choices, default=State.FREE)
    product_id = models.CharField(max_length=22, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
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
    r11 = models.BooleanField()
    r12 = models.BooleanField()
    device_r1 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r1')
    device_r2 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r2')
    device_r3 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r3')
    device_r4 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r4')
    device_r5 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r5')
    device_r6 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r6')
    device_r7 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r7')
    device_r8 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r8')
    device_r9 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='relay_device_r9')
    device_r10 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay_device_r10')
    device_r11 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay_device_r11')
    device_r12 = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='relay_device_r12')

    def reset(self):
        self.r1 = False
        self.r2 = False
        self.r3 = False
        self.r4 = False
        self.r5 = False
        self.r6 = False
        self.r7 = False
        self.r8 = False
        self.r9 = False
        self.r10 = False
        self.r11 = False
        self.r12 = False

        self.device_r1 = None
        self.device_r2 = None
        self.device_r3 = None
        self.device_r4 = None
        self.device_r5 = None
        self.device_r6 = None
        self.device_r7 = None
        self.device_r8 = None
        self.device_r9 = None
        self.device_r10 = None
        self.device_r11 = None
        self.device_r12 = None
