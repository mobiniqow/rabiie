from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """
        Create and save a User with the given phone and password.
        """
        if not phone:
            raise ValueError(_("The Phone Number field must be set"))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password)
        user.role = User.Role.ADMIN
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.IntegerChoices):
        USER = 1
        ADMIN = 5

    phone = models.CharField(max_length=15, unique=True, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    objects = UserManager()
    role = models.IntegerField(
        choices=Role.choices, default=Role.USER, verbose_name="نقش"
    )
    is_staff = models.BooleanField(default=False, verbose_name="کارمند")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone
