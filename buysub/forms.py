from django import forms
from django.utils.translation import ugettext_lazy as _


class ChooseSubscribeForm(forms.Form):
    choices_sub = (('10', '10 days'),
                   ('30', '30 days'), ('90', '90 days'))
    sub_type = forms.CharField(label=_('Choose tariff'), widget=forms.Select(choices=choices_sub), required=False)


class ConfirmSubscribeForm(forms.Form):
    confirm_sub = forms.CharField(label=_("Confirm"), widget=forms.CheckboxInput)
