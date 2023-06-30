from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    steamid = models.CharField(_('steamid'), unique=True, max_length=20)
    nickname = models.CharField(max_length=100, default="Hello")
    password = models.CharField(max_length=100, default=12340987)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_balance = models.DecimalField(default=0, max_digits=10, decimal_places=4)
    full_avatar = models.CharField(max_length=250, default="Failed to load img")
    medium_avatar = models.CharField(max_length=250, default="Failed to load img")

    USERNAME_FIELD = 'steamid'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.steamid