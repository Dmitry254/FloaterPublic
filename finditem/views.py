from django.shortcuts import render
from .find_item import start_script_for_market, start_script_for_bit
from .forms import ChooseShopForm, FindItemForm, FindItemSortForm
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def find_item(request):
    demo = False
    market_result = bit_result = None
    set_name = FindItemForm(request.GET)
    choice_shop = ChooseShopForm(request.GET)
    sorting_items = FindItemSortForm(request.GET)
    if request.user.is_authenticated:
        try:
            Subscribers.objects.get(steamid=request.user.steamid)
            if set_name.is_valid():
                if set_name.cleaned_data["search_names"]:
                    if sorting_items.is_valid():
                        if sorting_items.cleaned_data["sorting_items"]:
                            sort_type = sorting_items.cleaned_data["sorting_items"]
                            item_name = set_name.cleaned_data["search_names"]
                            if choice_shop.is_valid():
                                if choice_shop.cleaned_data["choice_shop"] == 'market':
                                    market_result = start_script_for_market(item_name, sort_type)
                                elif choice_shop.cleaned_data["choice_shop"] == 'bit':
                                    bit_result = start_script_for_bit(item_name, sort_type)
                                elif choice_shop.cleaned_data["choice_shop"] == 'market_bit':
                                    market_result = start_script_for_market(item_name, sort_type)
                                    bit_result = start_script_for_bit(item_name, sort_type)
        except ObjectDoesNotExist:
            demo = True
    else:
        demo = True
    return render(request, 'main/find_item.html', {'title': 'Find item', 'demo': demo,
                                                   'set_name': set_name, 'choice_shop': choice_shop,
                                                   'sorting_items': sorting_items,
                                                   'market_result': market_result, 'bit_result': bit_result})
