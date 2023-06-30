# Generated by Django 3.0.8 on 2020-07-13 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketFloatItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_item_name', models.CharField(max_length=100, verbose_name='Название предмета')),
                ('market_item_link', models.CharField(max_length=150, verbose_name='Ссылка на предмет')),
                ('market_item_float', models.FloatField(verbose_name='Флоат предмета')),
                ('market_item_price', models.FloatField(verbose_name='Цена предмета')),
                ('market_item_avg_price', models.FloatField(verbose_name='Средняя цена предмета')),
            ],
            options={
                'verbose_name': 'Флоат вещи маркета',
                'verbose_name_plural': 'Флоат вещей маркета',
            },
        ),
    ]