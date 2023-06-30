from django import forms
from .models import BitPatternItem
from django.utils.translation import ugettext_lazy as _


class BitFloatSort(forms.Form):
    min_float = forms.FloatField(label=_("Min"), required=False)
    max_float = forms.FloatField(label=_("Max"), required=False)


class BitPriceSort(forms.Form):
    min_price = forms.FloatField(label=_("Min"), required=False)
    max_price = forms.FloatField(label=_("Max"), required=False)


class BitAverageSort(forms.Form):
    min_average = forms.FloatField(label=_("Min"), required=False)
    max_average = forms.FloatField(label=_("Max"), required=False)


class BitSearchName(forms.Form):
    search_names = forms.CharField(label=_('Name'), required=False)


class BitSearchSeed(forms.Form):
    search_seeds = forms.CharField(label=_('Seed'), required=False)


class BitSearchPhase(forms.Form):
    search_phases = forms.CharField(label=_('Phase'), required=False)


class BitSortFilter(forms.Form):
    choices_sorts = (('bit_item_name', _('A-Z')),
                     ('bit_item_float', _('Increase float')), ('-bit_item_float', _('Decrease float')),
                     ('bit_item_price', _('Increase price')), ('-bit_item_price', _('Decrease price')))
    sorting_items = forms.CharField(label=_('Sort by'), widget=forms.Select(choices=choices_sorts), required=False)
