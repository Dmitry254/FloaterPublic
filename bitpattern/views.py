from django.shortcuts import render
from .models import BitPatternItem
from .forms import BitPatternItem, BitSortFilter, BitFloatSort, BitSearchName, BitSearchPhase, BitSearchSeed, BitAverageSort, BitPriceSort
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def bit_patterns(request):
    demo = False
    patterns = BitPatternItem.objects.order_by("bit_item_name")
    float_sort = BitFloatSort(request.GET)
    price_sort = BitPriceSort(request.GET)
    average_sort = BitAverageSort(request.GET)
    sort_filter = BitSortFilter(request.GET)
    search_names = BitSearchName(request.GET)
    search_seeds = BitSearchSeed(request.GET)
    search_phases = BitSearchPhase(request.GET)
    if request.user.is_authenticated:
        try:
            Subscribers.objects.get(steamid=request.user.steamid)
        except ObjectDoesNotExist:
            patterns = patterns.filter(bit_item_price__lte=4.5)
            demo = True
    else:
        patterns = patterns.filter(bit_item_price__lte=4.5)
        demo = True
    if sort_filter.is_valid():
        if sort_filter.cleaned_data["sorting_items"]:
            patterns = BitPatternItem.objects.order_by(sort_filter.cleaned_data["sorting_items"])
    if float_sort.is_valid():
        if float_sort.cleaned_data["min_float"]:
            patterns = patterns.filter(bit_item_float__gte=float_sort.cleaned_data["min_float"])
        if float_sort.cleaned_data["max_float"]:
            patterns = patterns.filter(bit_item_float__lte=float_sort.cleaned_data["max_float"])
    if price_sort.is_valid():
        if price_sort.cleaned_data["min_price"]:
            patterns = patterns.filter(bit_item_price__gte=price_sort.cleaned_data["min_price"])
        if price_sort.cleaned_data["max_price"]:
            patterns = patterns.filter(bit_item_price__lte=price_sort.cleaned_data["max_price"])
    if average_sort.is_valid():
        if average_sort.cleaned_data["min_average"]:
            patterns = patterns.filter(bit_item_avg_price__gte=average_sort.cleaned_data["min_average"])
        if average_sort.cleaned_data["max_average"]:
            patterns = patterns.filter(bit_item_avg_price__lte=average_sort.cleaned_data["max_average"])
    if search_names.is_valid():
        if search_names.cleaned_data["search_names"]:
            patterns = patterns.filter(bit_item_name__contains=search_names.cleaned_data["search_names"])
    if search_seeds.is_valid():
        if search_seeds.cleaned_data["search_seeds"]:
            patterns = patterns.filter(bit_item_seed__contains=search_seeds.cleaned_data["search_seeds"])
    if search_phases.is_valid():
        if search_phases.cleaned_data["search_phases"]:
            patterns = patterns.filter(bit_item_phase__contains=search_phases.cleaned_data["search_phases"])

    return render(request, 'main/bit_patterns.html', {'title': 'Bitskins patterns', 'patterns': patterns, 'demo': demo,
                                                      'float_sort': float_sort, 'search_names': search_names,
                                                      'search_seeds': search_seeds, 'search_phases': search_phases,
                                                      'sort_filter': sort_filter, 'price_sort': price_sort,
                                                      'average_sort': average_sort})
