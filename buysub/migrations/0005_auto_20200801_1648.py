# Generated by Django 3.0.8 on 2020-08-01 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buysub', '0004_auto_20200801_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 1, 16, 48, 6, 662625)),
        ),
        migrations.AlterField(
            model_name='userbuysubscribe',
            name='buy_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 1, 16, 48, 6, 663626), verbose_name='date'),
        ),
    ]
