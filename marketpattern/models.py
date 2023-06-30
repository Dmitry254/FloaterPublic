from django.db import models


class MarketPatternItem(models.Model):
    market_item_name = models.CharField('Название предмета', max_length=100)
    market_item_link = models.CharField('Ссылка на предмет', max_length=250)
    market_item_float = models.FloatField('Флоат предмета')
    market_item_seed = models.CharField('Seed предмета', max_length=10)
    market_item_phase = models.CharField('Фаза предмета', max_length=50)
    market_item_price = models.FloatField('Цена предмета')
    market_item_avg_price = models.FloatField('Средняя цена предмета')

    def __str__(self):
        return self.market_item_name

    class Meta:
        verbose_name = 'Паттерн вещи маркета'
        verbose_name_plural = 'Паттерн вещей маркета'

