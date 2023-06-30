from django import forms
from django.utils.translation import ugettext_lazy as _


class FindItemForm(forms.Form):
    search_names = forms.CharField(label=_('Name'), required=False)


class ChooseShopForm(forms.Form):
    choices_shops = (('market', 'Market CS:GO'), ('bit', 'BitSkins'),  ('market_bit', _('Market CS:GO and BitSkins')))
    choice_shop = forms.CharField(label=_('Shop'), widget=forms.Select(choices=choices_shops), required=False)


class FindItemSortForm(forms.Form):
    choices_sorts = (('min_float', _('Increase float')), ('max_float', _('Decrease float')),
                    ('min_price', _('Increase price')), ('max_price', _('Decrease price')))
    sorting_items = forms.CharField(label=_('Sort by'), widget=forms.Select(choices=choices_sorts), required=False)
