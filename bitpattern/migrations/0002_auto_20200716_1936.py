# Generated by Django 3.0.8 on 2020-07-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpattern', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitpatternitem',
            name='bit_item_seed',
            field=models.CharField(max_length=10, verbose_name='Seed предмета'),
        ),
    ]