from django.contrib import admin
from .models import MarketPatternItem
from .market_patterns import market_start_parsing


def market_make_reload(modeladmin, request, queryset):
    market_start_parsing()
market_make_reload.short_description = "Обновить базу вещей"


class MarketPatternItemAdmin(admin.ModelAdmin):
    list_display = ('market_item_name', 'market_item_float', 'market_item_seed', 'market_item_phase',
                    'market_item_price', 'market_item_avg_price')
    actions = [market_make_reload]


admin.site.register(MarketPatternItem, MarketPatternItemAdmin)
