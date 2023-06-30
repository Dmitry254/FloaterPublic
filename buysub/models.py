from django.db import models


class Subscribers(models.Model):
    steamid = models.CharField(unique=True, max_length=20)
    start_date = models.DateTimeField('Date')
    end_date = models.DateTimeField()


class UserBuySubscribe(models.Model):
    steamid = models.CharField(max_length=20)
    amount = models.PositiveIntegerField('Amount', default=0)
    buy_time = models.DateTimeField('Date')
