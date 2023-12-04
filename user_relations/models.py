from django.db import models

from account.models import User
from device.models import BaseModel


class UserChild(BaseModel):
    class State(models.IntegerChoices):
        ACTIVE = 1
        STOP = 2
        BANNED = 3
        REPORTED = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child')
