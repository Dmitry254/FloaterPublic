from django.shortcuts import render
from .models import MarketPatternItem
from .forms import MarketPatternItem, MarketSortFilter, MarketFloatSort, MarketSearchName, MarketSearchPhase, MarketSearchSeed,\
                    MarketPriceSort, MarketAverageSort
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def market_patterns(request):
    demo = False
    patterns = MarketPatternItem.objects.order_by("market_item_name")
    float_sort = MarketFloatSort(request.GET)
    price_sort = MarketPriceSort(request.GET)
    average_sort = MarketAverageSort(request.GET)
    sort_filter = MarketSortFilter(request.GET)
    search_names = MarketSearchName(request.GET)
    search_seeds = MarketSearchSeed(request.GET)
    search_phases = MarketSearchPhase(request.GET)
    if request.user.is_authenticated:
        try:
            Subscribers.objects.get(steamid=request.user.steamid)
        except ObjectDoesNotExist:
            patterns = patterns.filter(market_item_price__lte=300)
            demo = True
    else:
        patterns = patterns.filter(market_item_price__lte=300)
        demo = True
    if sort_filter.is_valid():
        if sort_filter.cleaned_data["sorting_items"]:
            patterns = MarketPatternItem.objects.order_by(sort_filter.cleaned_data["sorting_items"])
    if float_sort.is_valid():
        if float_sort.cleaned_data["min_float"]:
            patterns = patterns.filter(market_item_float__gte=float_sort.cleaned_data["min_float"])
        if float_sort.cleaned_data["max_float"]:
            patterns = patterns.filter(market_item_float__lte=float_sort.cleaned_data["max_float"])
    if price_sort.is_valid():
        if price_sort.cleaned_data["min_price"]:
            patterns = patterns.filter(market_item_price__gte=price_sort.cleaned_data["min_price"])
        if price_sort.cleaned_data["max_price"]:
            patterns = patterns.filter(market_item_price__lte=price_sort.cleaned_data["max_price"])
    if average_sort.is_valid():
        if average_sort.cleaned_data["min_average"]:
            patterns = patterns.filter(market_item_avg_price__gte=average_sort.cleaned_data["min_average"])
        if average_sort.cleaned_data["max_average"]:
            patterns = patterns.filter(market_item_avg_price__lte=average_sort.cleaned_data["max_average"])
    if search_names.is_valid():
        if search_names.cleaned_data["search_names"]:
            patterns = patterns.filter(market_item_name__contains=search_names.cleaned_data["search_names"])
    if search_seeds.is_valid():
        if search_seeds.cleaned_data["search_seeds"]:
            patterns = patterns.filter(market_item_seed__contains=search_seeds.cleaned_data["search_seeds"])
    if search_phases.is_valid():
        if search_phases.cleaned_data["search_phases"]:
            patterns = patterns.filter(market_item_phase__contains=search_phases.cleaned_data["search_phases"])

    return render(request, 'main/market_patterns.html', {'title': 'Market patterns', 'demo': demo,
                                                         'patterns': patterns, 'float_sort': float_sort,
                                                         'search_names': search_names, 'search_seeds': search_seeds,
                                                         'search_phases': search_phases, 'sort_filter': sort_filter,
                                                         'price_sort': price_sort, 'average_sort': average_sort})

