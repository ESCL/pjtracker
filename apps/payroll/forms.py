__author__ = 'kako'


from collections import OrderedDict
from decimal import Decimal

from django import forms
from django.utils.functional import cached_property

from ..common.forms import OwnedEntitiesForm, OwnedEntityForm
from .models import CalendarDay, HourType, HourTypeRange, Period, StandardHours


class CalendarDaySearchForm(OwnedEntitiesForm):
    name__icontains = forms.CharField(label='Name', required=False)
    date__gte = forms.DateField(label='From date', required=False)
    date__lte = forms.DateField(label='To date', required=False)


class HourTypeSearchForm(OwnedEntitiesForm):
    name__icontains = forms.CharField(label='Name', required=False)
    code__icontains = forms.CharField(label='Code', required=False)


class PeriodSearchForm(OwnedEntitiesForm):
    name__icontains = forms.CharField(label='Name', required=False)
    code__icontains = forms.CharField(label='Code', required=False)


class WorkedHoursSearchForm(OwnedEntitiesForm):
    pass


class HoursSettingsForm(OwnedEntitiesForm):

    DAY_TYPES = OrderedDict((
        ('weekdays', CalendarDay.WEEKDAY),
        ('saturdays', CalendarDay.SATURDAY),
        ('sundays', CalendarDay.SUNDAY),
        ('holidays', CalendarDay.PUBLIC_HOLIDAY)
    ))

    @cached_property
    def standard_hours(self):
        return {sh.day_type: sh for sh in
                StandardHours.objects.for_owner(self.user.owner)}

    @cached_property
    def hour_type_ranges(self):
        res = {}
        for htr in HourTypeRange.objects.for_owner(self.user.owner):
            if htr.day_type not in res:
                res[htr.day_type] = {}
            res[htr.day_type][htr.hour_type.code] = htr
        return res

    @cached_property
    def hour_types(self):
        return HourType.objects.for_owner(self.user.owner)

    def __init__(self, *args, **kwargs):
        super(HoursSettingsForm, self).__init__(*args, **kwargs)

        # Reset key order and create fields
        self.rows = []
        for day_type_name, day_type_code in self.DAY_TYPES.items():
            row = {'day_type_name': day_type_name, 'fields': []}

            # Standard hours field
            sh = self.standard_hours.get(day_type_code)
            hours = sh and sh.hours or 0
            fname = 'sh-{}'.format(day_type_name)
            self.fields[fname] = forms.DecimalField(initial=hours, required=False)
            row['fields'].append(self[fname])

            # Limit fields, iterate values
            for ht in self.hour_types:
                fname = 'htr-{}-{}'.format(day_type_name, ht.code)
                htr = self.hour_type_ranges.get(day_type_code, {}).get(ht.code)
                hours = htr and htr.limit or 0
                self.fields[fname] = forms.DecimalField(initial=hours, required=False)
                row['fields'].append(self[fname])

            # Append row
            self.rows.append(row)

    def _update_range(self, day_type_code, day_type_name, hour_type):
        """
        Update hour type range for the given day and hour type using parsed
        form data.

        :param day_type_code: code of day type
        :param day_type_name: name of day type
        :param day_type_code: hour type instance
        :return: None
        """
        # Get htr and posted limit
        htr = self.hour_type_ranges.get(day_type_code, {}).get(hour_type.code)
        htr_fname = 'htr-{}-{}'.format(day_type_name, hour_type.code)
        limit = self.cleaned_data.get(htr_fname)

        # Now process
        if htr and not limit:
            # Limit set to zero, delete instance
            htr.delete()

        elif limit:
            # Get or create hour type range and update limit
            if not htr:
                htr = HourTypeRange(day_type=day_type_code,
                                    hour_type=hour_type, owner=self.user.owner)
            htr.limit = limit
            htr.save()

    def clean(self):
        """
        Clean the fields, checking for two possible errors: having two hour
        types in the same day type with the same limit, and having no hour
        type limit higher than the standard hours for a day type.
        """
        cleaned_data = super(HoursSettingsForm, self).clean()

        # Compare standard hours and limits for every day type
        for day_type_name in self.DAY_TYPES.keys():
            # Get standard hours for day type (default to zero)
            sh_fname = 'sh-{}'.format(day_type_name)
            std_hours = cleaned_data.get(sh_fname) or 0

            # Now check all the limits
            limits = [0]
            for ht in self.hour_types:
                # Get limit for that hour type
                htr_fname = 'htr-{}-{}'.format(day_type_name, ht.code)
                limit = cleaned_data.get(htr_fname)

                # Make sure every non-zero limit is unique
                if limit and limit in limits:
                    cleaned_data.pop(htr_fname)
                    self.add_error(sh_fname, forms.ValidationError(
                        'Limits cannot be repeated in the same day type.'
                    ))
                elif limit:
                    limits.append(limit)

            # Now make sure the max limit in the day is greater than standard hours
            # (at least 50% greater)
            if max(limits) < std_hours * Decimal(1.5):
                cleaned_data.pop(sh_fname, None)
                self.add_error(sh_fname, forms.ValidationError(
                    'One of the hour type limits must be at least 50% '
                    'greater than the average.'
                ))

        # Now return cleaned data
        return cleaned_data

    def save(self):
        """
        Save the standard hours and hour type ranges that have changed.
        """
        # Compare standard hours and limits for every day type
        for day_type_name, day_type_code in self.DAY_TYPES.items():
            # Get standard hours for day type (default to zero)
            sh_fname = 'sh-{}'.format(day_type_name)
            sh = self.standard_hours.get(day_type_code)

            # Get the std hours instance (or create new one), set hours and save
            if not sh:
                sh = StandardHours(day_type=day_type_code, owner=self.user.owner)
            std_hours = self.cleaned_data.get(sh_fname) or 0
            sh.hours = std_hours
            sh.save()

            # Update hour type ranges for day type
            for ht in self.hour_types:
                self._update_range(day_type_code, day_type_name, ht)

        # Now return true
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

    def clean(self):
        """
        Make sure forecast date is between start and end.
        """
        # Clean data and get all dates
        cleaned_data = super(PeriodForm, self).clean()
        start = cleaned_data.get('start_date')
        forecast_start = cleaned_data.get('forecast_start_date')
        end = cleaned_data.get('end_date')

        # If we have all dates, make sure forecast is between start and end
        if start and forecast_start and end and \
                not start <= forecast_start <= end:
            cleaned_data.pop('forecast_start_date')
            raise forms.ValidationError(
                'Invalid dates, forecast must be after start date'
                'and before end date.'
            )

        # Return all cleaned data
        return cleaned_data


class ProcessPayrollForm(forms.Form):

    confirm = forms.ChoiceField(label='Are you sure you want to do that?',
                                choices=(('no', "No"), ('yes', "Yes")))

    def clean_confirm(self):
        """
        Clean confirm field, advising user to go back.
        """
        if self.cleaned_data.get('confirm') != 'yes':
            self.cleaned_data.pop('confirm')
            raise forms.ValidationError("If you're not sure click on Cancel instead.")
