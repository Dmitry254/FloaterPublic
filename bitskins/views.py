from django.shortcuts import render
from .forms import BitFloatSort, BitSearchName, BitSortFilter, BitPriceSort, BitAverageSort
from .models import BitFloatItem
from buysub.models import Subscribers
from main.help_defs import base_view
from django.core.exceptions import ObjectDoesNotExist


@base_view
def bit_float(request):
    demo = False
    floats = BitFloatItem.objects.order_by("bit_item_name")
    float_sort = BitFloatSort(request.GET)
    price_sort = BitPriceSort(request.GET)
    average_sort = BitAverageSort(request.GET)
    sort_filter = BitSortFilter(request.GET)
    search = BitSearchName(request.GET)
    if request.user.is_authenticated:
        try:
            Subscribers.objects.get(steamid=request.user.steamid)
        except ObjectDoesNotExist:
            floats = floats.filter(bit_item_price__lte=4.5)
            demo = True
    else:
        floats = floats.filter(bit_item_price__lte=4.5)
        demo = True
    if sort_filter.is_valid():
        if sort_filter.cleaned_data["sorting_items"]:
            floats = BitFloatItem.objects.order_by(sort_filter.cleaned_data["sorting_items"])
    if float_sort.is_valid():
        if float_sort.cleaned_data["min_float"]:
            floats = floats.filter(bit_item_float__gte=float_sort.cleaned_data["min_float"])
        if float_sort.cleaned_data["max_float"]:
            floats = floats.filter(bit_item_float__lte=float_sort.cleaned_data["max_float"])
    if price_sort.is_valid():
        if price_sort.cleaned_data["min_price"]:
            floats = floats.filter(bit_item_price__gte=price_sort.cleaned_data["min_price"])
        if price_sort.cleaned_data["max_price"]:
            floats = floats.filter(bit_item_price__lte=price_sort.cleaned_data["max_price"])
    if average_sort.is_valid():
        if average_sort.cleaned_data["min_average"]:
            floats = floats.filter(bit_item_avg_price__gte=average_sort.cleaned_data["min_average"])
        if average_sort.cleaned_data["max_average"]:
            floats = floats.filter(bit_item_avg_price__lte=average_sort.cleaned_data["max_average"])
    if search.is_valid():
        if search.cleaned_data["search_names"]:
            floats = floats.filter(bit_item_name__contains=search.cleaned_data["search_names"])

    return render(request, 'main/bit_float.html', {'title': 'Bitskins floats', 'floats': floats, 'demo': demo,
                                                   'float_sort': float_sort, 'search': search,
                                                   'sort_filter': sort_filter, 'price_sort': price_sort,
                                                   'average_sort': average_sort})
