from django.contrib import admin
from .models import BitFloatItem
from .bit_float import bit_start_parsing


def bit_make_reload(modeladmin, request, queryset):
    bit_start_parsing()
bit_make_reload.short_description = "Обновить базу вещей"


class BitFloatItemAdmin(admin.ModelAdmin):
    list_display = ('bit_item_name', 'bit_item_float', 'bit_item_price', 'bit_item_avg_price')
    actions = [bit_make_reload]


admin.site.register(BitFloatItem, BitFloatItemAdmin)
