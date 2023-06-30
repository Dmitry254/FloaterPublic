from django.db import models


class BitPatternItem(models.Model):
    bit_item_name = models.CharField('Название предмета', max_length=100)
    bit_item_link = models.CharField('Ссылка на предмет', max_length=250)
    bit_item_float = models.FloatField('Флоат предмета')
    bit_item_seed = models.CharField('Seed предмета', max_length=10)
    bit_item_phase = models.CharField('Фаза предмета', max_length=50)
    bit_item_price = models.FloatField('Цена предмета')
    bit_item_avg_price = models.FloatField('Средняя цена предмета')

    def __str__(self):
        return self.bit_item_name

    class Meta:
        verbose_name = 'Паттерн вещи битскинза'
        verbose_name_plural = 'Паттерн вещей битскинза'
