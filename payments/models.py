from django.db import models
from django.utils.timezone import datetime


class UserBalanceChange(models.Model):
    steamid = models.CharField(max_length=20)
    amount = models.PositiveIntegerField('Amount', default=0)
    datetime = models.DateTimeField('date', default=datetime.now)
