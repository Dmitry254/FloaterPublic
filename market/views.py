from django.shortcuts import render
from .forms import MarketFloatSort, MarketPriceSort, MarketAverageSort, MarketSearchName, MarketSortFilter, MarketAvgCompare
from .models import MarketFloatItem
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def market_float(request):
    demo = False
    floats = MarketFloatItem.objects.order_by("market_item_name")
    float_sort = MarketFloatSort(request.GET)
    sort_filter = MarketSortFilter(request.GET)
    search = MarketSearchName(request.GET)
    price_sort = MarketPriceSort(request.GET)
    average_sort = MarketAverageSort(request.GET)
    avg_compare = MarketAvgCompare(request.GET)
    if request.user.is_authenticated:
        try:
            Subscribers.objects.get(steamid=request.user.steamid)
        except ObjectDoesNotExist:
            floats = floats.filter(market_item_price__lte=300)
            demo = True
    else:
        floats = floats.filter(market_item_price__lte=300)
        demo = True
    if sort_filter.is_valid():
        if sort_filter.cleaned_data["sorting_items"]:
            floats = MarketFloatItem.objects.order_by(sort_filter.cleaned_data["sorting_items"])
    if float_sort.is_valid():
        if float_sort.cleaned_data["min_float"]:
            floats = floats.filter(market_item_float__gte=float_sort.cleaned_data["min_float"])
        if float_sort.cleaned_data["max_float"]:
            floats = floats.filter(market_item_float__lte=float_sort.cleaned_data["max_float"])
    if price_sort.is_valid():
        if price_sort.cleaned_data["min_price"]:
            floats = floats.filter(market_item_price__gte=price_sort.cleaned_data["min_price"])
        if price_sort.cleaned_data["max_price"]:
            floats = floats.filter(market_item_price__lte=price_sort.cleaned_data["max_price"])
    if average_sort.is_valid():
        if average_sort.cleaned_data["min_average"]:
            floats = floats.filter(market_item_avg_price__gte=average_sort.cleaned_data["min_average"])
        if average_sort.cleaned_data["max_average"]:
            floats = floats.filter(market_item_avg_price__lte=average_sort.cleaned_data["max_average"])
    if search.is_valid():
        if search.cleaned_data["search_names"]:
            floats = floats.filter(market_item_name__contains=search.cleaned_data["search_names"])

    return render(request, 'main/market_float.html', {'title': 'Market floats', 'demo': demo,
     'floats': floats, 'float_sort': float_sort, 'price_sort': price_sort, 'average_sort': average_sort,
                                                      'search': search, 'sort_filter': sort_filter})
