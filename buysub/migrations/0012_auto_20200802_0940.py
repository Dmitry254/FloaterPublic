# Generated by Django 3.0.8 on 2020-08-02 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buysub', '0011_auto_20200802_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='start_date',
            field=models.DateTimeField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='userbuysubscribe',
            name='buy_time',
            field=models.DateTimeField(verbose_name='Date'),
        ),
    ]