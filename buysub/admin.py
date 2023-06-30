from django.contrib import admin
from .models import Subscribers, UserBuySubscribe
from django.utils import timezone


def delete_subscribers(modeladmin, request, queryset):
    stop_sub = Subscribers.objects.all().filter(end_date__lte=timezone.now())
    stop_sub.delete()
delete_subscribers.short_description = "Удалить истекшие подписки"

class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('steamid', 'start_date', 'end_date')
    actions = [delete_subscribers]

class UserBuySubscribeAdmin(admin.ModelAdmin):
    list_display = ('steamid', 'amount', 'buy_time')

admin.site.register(Subscribers, SubscribersAdmin)

admin.site.register(UserBuySubscribe, UserBuySubscribeAdmin)
