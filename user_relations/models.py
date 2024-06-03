from django.db import models
from authenticate.models import User


class UserChild(models.Model):
    class State(models.IntegerChoices):
        ACTIVE = 1
        STOP = 2
        BANNED = 3
        REPORTED = 4

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name="child")
