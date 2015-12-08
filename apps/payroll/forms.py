__author__ = 'kako'

from collections import OrderedDict

from django import forms
from django.utils.functional import cached_property

from ..common.forms import ModernForm, OwnedEntityForm
from .models import CalendarDay, HourType, Period, StandardHours


class CalendarDaySearchForm(ModernForm):
    name__icontains = forms.CharField(label='Name', required=False)
    date__gte = forms.DateField(label='From date', required=False)
    date__lte = forms.DateField(label='To date', required=False)


class HourTypeSearchForm(ModernForm):
    name__icontains = forms.CharField(label='Name', required=False)
    code__icontains = forms.CharField(label='Code', required=False)


class PeriodSearchForm(ModernForm):
    name__icontains = forms.CharField(label='Name', required=False)
    code__icontains = forms.CharField(label='Code', required=False)


class StandardHoursForm(forms.Form):

    FIELD_DAY_TYPE = OrderedDict((
        ('weekdays', CalendarDay.WEEKDAY),
        ('saturdays', CalendarDay.SATURDAY),
        ('sundays', CalendarDay.SUNDAY),
        ('holidays', CalendarDay.PUBLIC_HOLIDAY)
    ))

    @cached_property
    def values(self):
        return {sh.day_type: sh for sh in
                StandardHours.objects.for_owner(self.account)}

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super(StandardHoursForm, self).__init__(*args, **kwargs)
        for f, day_type in self.FIELD_DAY_TYPE.items():
            sh = self.values.get(day_type)
            self.fields[f] = forms.DecimalField(initial=sh and sh.hours or 0)

        self.fields.keyOrder = self.FIELD_DAY_TYPE.keys()

    def clean(self):
        cleaned_data = super(StandardHoursForm, self).clean()
        for k, v in cleaned_data.items():
            day_type = self.FIELD_DAY_TYPE.get(k)
            if not day_type:
                self.add_error(k, forms.ValidationError('Day type not recognized'))
                cleaned_data.pop(k)
        return cleaned_data

    def save(self):
        """
        Save the standard hours forms.
        """
        for k, v in self.cleaned_data.items():
            day_type = self.FIELD_DAY_TYPE.get(k)
            sh = self.values.get(day_type)
            if not sh:
                sh = StandardHours(day_type=day_type, owner=self.account)
            sh.hours = v
            sh.save()

        # Nothing to return
        return True


class CalendarDayForm(OwnedEntityForm):

    class Meta:
        model = CalendarDay
        exclude = ('owner',)


class HourTypeForm(OwnedEntityForm):

    class Meta:
        model = HourType
        exclude = ('owner',)


class PeriodForm(OwnedEntityForm):

    class Meta:
        model = Period
        exclude = ('owner', 'code',)
