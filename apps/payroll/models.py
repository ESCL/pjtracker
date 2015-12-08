from datetime import date, timedelta

from django.db import models

from ..common.db.models import OwnedEntity
from ..deployment.models import WorkLog, TimeSheet
from .query import CalendarDayQuerySet


class CalendarDay(OwnedEntity):

    PUBLIC_HOLIDAY = 'PH'
    NATIONAL_HOLIDAY = 'NH'
    STATE_HOLIDAY = 'SH'

    WEEKDAY = 'WD'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    objects = CalendarDayQuerySet.as_manager()

    date = models.DateField(
        default=date.today
    )
    name = models.CharField(
        max_length=128
    )
    type = models.CharField(
        max_length=3,
        db_index=True,
        choices=((PUBLIC_HOLIDAY, 'Public Holiday'),
                 (NATIONAL_HOLIDAY, 'National Holiday'),
                 (STATE_HOLIDAY, 'State Holiday'))
    )

    def __init__(self, *args, **kwargs):
        super(CalendarDay, self).__init__(*args, **kwargs)
        if not self.type in (self.PUBLIC_HOLIDAY,):
            self.type = self._determine_type()

    def __cmp__(self, other):
        return self.date.__cmp__(other.date)

    def __eq__(self, other):
        return self.date == other.date

    def __lt__(self, other):
        return self.date.__lt__(other.date)

    def __gt__(self, other):
        return self.date.__gt__(other.date)

    def _determine_type(self):
        return {6: self.SATURDAY, 7: self.SUNDAY}.get(self.date.isoweekday(), self.WEEKDAY)

    def is_a(self, day_type):
        return self.type == day_type


class HourType(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=6
    )

    def __str__(self):
        return self.name


class DayTypeBase(OwnedEntity):
    """
    Base class for models that have a day_type field.
    """
    class Meta:
       abstract = True

    day_type = models.CharField(
        max_length=3,
        choices=((CalendarDay.WEEKDAY, 'Weekday'),
                 (CalendarDay.SATURDAY, 'Saturday'),
                 (CalendarDay.SUNDAY, 'Sunday'),
                 (CalendarDay.PUBLIC_HOLIDAY, 'Public Holiday'),
                 (CalendarDay.NATIONAL_HOLIDAY, 'National Holiday'),
                 (CalendarDay.STATE_HOLIDAY, 'State Holiday'))
    )


class HourTypeRange(DayTypeBase):

    class Meta:
        ordering = ('day_type', 'limit',)

    limit = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        default=24
    )
    hour_type = models.ForeignKey(
        'HourType'
    )

    def __str__(self):
        return '{} {}'.format(self.day_type, self.hour_type)


class StandardHours(DayTypeBase):

    class Meta:
        unique_together = ('owner', 'day_type',)

    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4,
    )


class Period(OwnedEntity):

    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=10,
    )
    start_date = models.DateField(
    )
    end_date = models.DateField(
    )
    forecast_start_date = models.DateField(
    )

    def save(self, *args, **kwargs):
        self.code = '{:%Y-%m}'.format(self.start_date)
        if not self.name:
            self.name = '{:%b %Y}'.format(self.start_date)

        return super(Period, self).save(*args, **kwargs)


class WorkedHours(OwnedEntity):

    PHASE_ACTUAL = 'A'
    PHASE_FORECAST = 'F'
    PHASE_RETROACTIVE = 'R'

    period = models.ForeignKey(
        'Period'
    )
    phase = models.CharField(
        max_length=1,
        db_index=True,
        choices=((PHASE_ACTUAL, 'Actual'),
                 (PHASE_FORECAST, 'Forecast'),
                 (PHASE_RETROACTIVE, 'Retroactive'))
    )
    employee = models.ForeignKey(
        'resources.Employee'
    )
    hour_type = models.ForeignKey(
        'HourType'
    )
    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4
    )

    @staticmethod
    def get_day_ranges(owner):
        """
        Get a dictionary of ranges per day type, where ranges is a list of
        hour type ranges to apply in sequence (the order MUST be respected).
        """
        day_ranges = {}
        for range in HourTypeRange.objects.for_owner(owner):
            if range.day_type not in day_ranges:
                day_ranges[range.day_type] = []
            day_ranges[range.day_type].append(range)
        return day_ranges

    @staticmethod
    def split_hours_per_type(hours, ranges):
        """
        Get a dictionary of hours per hour type, determined by applying the
        given hour type ranges to the given hours.
        """
        hpt = {}
        limit = 0
        for r in ranges:
            # Get hours, sliced to respect both limits
            h = min(max(hours - limit, 0), r.limit)

            if h:
                # Hours are not zero, add them
                if r.hour_type not in hpt:
                    hpt[r.hour_type] = 0
                hpt[r.hour_type] += h

            # Update limit for next one
            limit = r.limit or 0

        # Return split
        return hpt

    @classmethod
    def calculate(cls, period, phase, employee):
        """
        Get new WorkedHours instances for the given period, employee and phase.
        """
        if phase == cls.PHASE_FORECAST:
            # Forecast phase, calculate directly
            hours_per_type = cls._calculate_forecast(employee, period.forecast_start_date,
                                                     period.end_date)

        else:
            # One of actuals, first determine dates
            if phase == cls.PHASE_ACTUAL:
                start = period.start_date
                end = period.forecast_start_date - timedelta(days=1)
            else:
                start = period.start_date
                end = period.forecast_start_date - timedelta(days=1)

            # Now calculate
            hours_per_type = cls._calculate_actual(employee, start, end)

        # Now return the list, one per type:hours
        return [cls(employee=employee, period=period, phase=phase,
                    hour_type=ht, hours=h)
                for ht, h in hours_per_type.items()]

    @classmethod
    def _calculate_actual(cls, employee, start_date, end_date):
        # Get hour type ranges per day type
        day_ranges = cls.get_day_ranges(employee.owner)

        # Get all the days in the range (stored or not)
        days = CalendarDay.objects.in_range(start_date, end_date)

        # Get the hours per day (actual values)
        groups = WorkLog.objects.filter(
            resource=employee.resource_ptr,
            timesheet__status=TimeSheet.STATUS_APPROVED,
            timesheet__date__gte=start_date,
            timesheet__date__lte=end_date
        )

        # Now collect hours per hour type
        hours_per_type = {}
        for wlg in groups.values('timesheet__date').annotate(hours=models.Sum('hours')):
            day = days[wlg.timesheet.date]
            hpt = cls.split_hours_per_type(wlg.hours, day_ranges[day.type])
            for ht, h in hpt.items():
                hours_per_type[ht] = hours_per_type.get(ht, 0) + h

        return hours_per_type

    @classmethod
    def _calculate_forecast(cls, employee, start_date, end_date):
        # Get hour type ranges per day type
        day_ranges = cls.get_day_ranges(employee.owner)

        # Get all the days in the range (stored or not)
        days = CalendarDay.objects.in_range(start_date, end_date)

        # Get hours per day (estimated values)
        # TODO: abstract this away to allow using other methods
        day_hours = {sh.day_type: sh.hours for sh in
                     StandardHours.objects.for_owner(employee.owner)}

        # Now collect hours per hour type
        hours_per_type = {}
        cur_date = start_date
        while cur_date <= end_date:
            day = days[cur_date]
            hpt = cls.split_hours_per_type(day_hours.get(day.type, 0),
                                           day_ranges[day.type])
            for ht, h in hpt.items():
                hours_per_type[ht] = hours_per_type.get(ht, 0) + h

            # Increase date
            cur_date += timedelta(days=1)

        return hours_per_type
