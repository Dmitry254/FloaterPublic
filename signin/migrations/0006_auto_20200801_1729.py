# Generated by Django 3.0.8 on 2020-08-01 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signin', '0005_auto_20200801_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_balance',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]
