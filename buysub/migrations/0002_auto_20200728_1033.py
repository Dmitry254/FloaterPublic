# Generated by Django 3.0.8 on 2020-07-28 01:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buysub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 28, 10, 33, 6, 705526)),
        ),
    ]
