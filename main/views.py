from django.shortcuts import render, redirect
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def index(request):
    return render(request, 'main/index.html', {'title': 'Floater'})


@base_view
def account(request):
    if request.user.is_authenticated:
        try:
            current_user = Subscribers.objects.get(steamid=request.user.steamid)
            date = current_user.end_date
            return render(request, 'main/account.html', {'title': 'Account', 'date': date})
        except ObjectDoesNotExist:
            return render(request, 'main/account.html', {'title': 'Account', 'date': "XX.XX.XXXX XX-XX"})
    else:
        return redirect('home')


@base_view
def add_funds(request):
    return render(request, 'main/add_funds.html', {'title': 'Add funds'})
