from django import forms
from .models import MarketPatternItem
from django.utils.translation import ugettext_lazy as _


class MarketFloatSort(forms.Form):
    min_float = forms.FloatField(label=_("Min"), required=False)
    max_float = forms.FloatField(label=_("Max"), required=False)


class MarketPriceSort(forms.Form):
    min_price = forms.FloatField(label=_("Min"), required=False)
    max_price = forms.FloatField(label=_("Max"), required=False)


class MarketAverageSort(forms.Form):
    min_average = forms.FloatField(label=_("Min"), required=False)
    max_average = forms.FloatField(label=_("Max"), required=False)


class MarketSearchName(forms.Form):
    search_names = forms.CharField(label=_('Name'), required=False)


class MarketSearchSeed(forms.Form):
    search_seeds = forms.CharField(label='Seed', required=False)


class MarketSearchPhase(forms.Form):
    search_phases = forms.CharField(label=_('Phase'), required=False)


class MarketSortFilter(forms.Form):
    choices_sorts = (('market_item_name', _('A-Z')),
                     ('market_item_float', _('Increase float')), ('-market_item_float', _('Decrease float')),
                     ('market_item_price', _('Increase price')), ('-market_item_price', _('Decrease price')))
    sorting_items = forms.CharField(label=_('Sort by'), widget=forms.Select(choices=choices_sorts), required=False)
