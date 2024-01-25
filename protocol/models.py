from django.db import models


class EVENT(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=100)
    address = models.CharField(max_length=25)
    input_output = models.BooleanField()
    ack = models.BooleanField(default=False)
    # user_device = models.ForeignKey(UserDevice, on_delete=models.SET_NULL, null=True)
