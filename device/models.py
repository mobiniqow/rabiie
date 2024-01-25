from django.db import models
import uuid

from authenticate.models import User


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
    t1 = models.JSONField(blank=True, null=True)
    t2 = models.JSONField(blank=True, null=True)
    t3 = models.JSONField(blank=True, null=True)
    t4 = models.JSONField(blank=True, null=True)
    t5 = models.JSONField(blank=True, null=True)
    t6 = models.JSONField(blank=True, null=True)
    r1 = models.BooleanField()
    r2 = models.BooleanField()
    r3 = models.BooleanField()
    r4 = models.BooleanField()
    r5 = models.BooleanField()
    r6 = models.BooleanField()

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


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=23)
    image = models.ImageField(upload_to='device/image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Relay12Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True)
    relay_id = models.ForeignKey(Relay12, on_delete=models.SET_NULL, null=True, blank=True)
    relay_port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.device.name

    class Meta:
        unique_together = ('device', 'relay_id', 'relay_port')
