from django.contrib import admin
from .models import UserBalanceChange


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('steamid', 'amount', 'end_date')


admin.site.register(UserBalanceChange)
