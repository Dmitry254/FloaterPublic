from .models import Subscribers, UserBuySubscribe
from django.shortcuts import render, redirect
from signin.models import CustomUser
from django.utils import timezone
from django.utils.timezone import datetime, timedelta


def add_subscriber(request, sub_type):
    error = ""
    if sub_type == '10':
        sum_pay = 2
    elif sub_type == '30':
        sum_pay = 5
    elif sub_type == '90':
        sum_pay = 13
    else:
        error = "unknown"
        return render(request, 'main/subscriptions.html', {'title': 'Repeat buy please', 'error': error})
    steamid = request.user.steamid
    custom_user = CustomUser.objects.get(steamid=steamid)
    if custom_user.user_balance - sum_pay >= 0:
        steamid = request.user.steamid
        try:
            sub_days = int(sub_type)
            user = Subscribers.objects.get(steamid=steamid)
            user.end_date = user.end_date + timedelta(days=sub_days)
            user.save()
        except Subscribers.DoesNotExist:
            end_date = timezone.now() + timedelta(days=sub_days)
            Subscribers.objects.create(steamid=steamid, start_date=datetime.now(), end_date=end_date)
        custom_user.user_balance = custom_user.user_balance - sum_pay
        custom_user.save()
        UserBuySubscribe.objects.create(steamid=steamid, amount=sum_pay, buy_time=datetime.now())
        return redirect('account')
    else:
        error = "balance"
        return render(request, 'main/subscriptions.html', {'title': 'Not enough balance', 'error': error})