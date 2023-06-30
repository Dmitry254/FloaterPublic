from django.shortcuts import render
from .buy_sub import add_subscriber
from .forms import ChooseSubscribeForm
from signin.models import CustomUser
from main.help_defs import base_view


@base_view
def subscriptions(request):
    sub_type = ChooseSubscribeForm(request.POST)
    if sub_type.is_valid():
        if sub_type.cleaned_data["sub_type"]:
            return render(request, 'main/confirm_buy.html', {'title': 'Confirm', 'sub_type': sub_type.cleaned_data["sub_type"]})
    return render(request, 'main/subscriptions.html', {'title': 'Subscribes', 'sub_type': sub_type})


@base_view
def confirm_buy(request):
    sub_type = request.get_full_path()
    sub_type = sub_type.replace("/en/confirm-buy?", "")
    sub_type = sub_type.replace("/ru/confirm-buy?", "")
    sub_type = sub_type[0:2]
    return add_subscriber(request, sub_type)
