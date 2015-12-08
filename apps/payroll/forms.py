__author__ = 'kako'

from django import forms

from ..common.forms import ModernForm, OwnedEntityForm
from .models import CalendarDay, HourType


class CalendarDaySearchForm(ModernForm):
    name__icontains = forms.CharField(label='Name')
    date__gte = forms.DateField(label='From date')
    date__lte = forms.DateField(label='To date')


class HourTypeSearchForm(ModernForm):
    name__icontains = forms.CharField(label='Name')
    code__icontains = forms.CharField(label='Code')


class CalendarDayForm(OwnedEntityForm):

    class Meta:
        model = CalendarDay
        exclude = ('owner',)


class HourTypeForm(OwnedEntityForm):

    class Meta:
        model = HourType
        exclude = ('owner',)
