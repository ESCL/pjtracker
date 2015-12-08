from datetime import date, timedelta

from django.db import models
from django.utils.functional import cached_property

from ..common.db.models import OwnedEntity
from ..deployment.models import WorkLog, TimeSheet
from .query import CalendarDayQuerySet


class CalendarDay(OwnedEntity):
    """
    Special day marked in a calendar. Due to the default behaviour provided by
    non-stored instances, usually only holidays need to be stored.
    """
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
        """
        Override to provide a default "type" if one is not provided.
        """
        super(CalendarDay, self).__init__(*args, **kwargs)
        if not self.type in (self.PUBLIC_HOLIDAY,):
            self.type = self._determine_type()

    # Magic methods to allow comparison: delegate to its date object

    def __cmp__(self, other):
        return self.date.__cmp__(other.date)

    def __eq__(self, other):
        return self.date == other.date

    def __lt__(self, other):
        return self.date.__lt__(other.date)

    def __gt__(self, other):
        return self.date.__gt__(other.date)

    # Helpers

    def _determine_type(self):
        return {6: self.SATURDAY, 7: self.SUNDAY}.get(self.date.isoweekday(), self.WEEKDAY)

    def is_a(self, day_type):
        return self.type == day_type


class HourType(OwnedEntity):
    """
    Type of hour, usually differentiated according to their pay rates.
    """
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
    """
    Rule to determine hour type based on day type and number of hours.
    """
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
    """
    Typical number of hours worked for a given day type, used for the simplest
    form of prediction.
    """
    class Meta:
        unique_together = ('owner', 'day_type',)

    hours = models.DecimalField(
        decimal_places=2,
        max_digits=4,
    )


class Period(OwnedEntity):
    """
    A "Payroll Month".
    """
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

    @cached_property
    def previous(self):
        return self.__class__.objects.for_owner(self.owner).get(end_date=self.start_date - timedelta(days=1))

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = '{:%Y-%m}'.format(self.start_date)
        if not self.name:
            self.name = '{:%b %Y}'.format(self.start_date)

        return super(Period, self).save(*args, **kwargs)


class WorkedHours(OwnedEntity):
    """
    Unique group of period:phase:employee:hour_type.

    Note: instances of this model SHOULD ONLY be created through this model's
    calculate class method.
    """
    PHASE_ADJUSTMENT = 'D'
    PHASE_ACTUAL = 'A'
    PHASE_FORECAST = 'F'
    PHASE_RETROACTIVE = 'R'

    period = models.ForeignKey(
        'Period'
    )
    phase = models.CharField(
        max_length=1,
        db_index=True,
        choices=((PHASE_ADJUSTMENT, 'Adjustment'),
                 (PHASE_ACTUAL, 'Actual'),
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
    def _get_actual_hours(days, employee, start_date, end_date):
        """
        Get the total actual hours per day for the given employee.
        """
        groups = WorkLog.objects.filter(
            resource=employee.resource_ptr,
            timesheet__status=TimeSheet.STATUS_APPROVED,
            timesheet__date__gte=start_date,
            timesheet__date__lte=end_date
        ).values('timesheet__date').annotate(hours=models.Sum('hours'))
        return {wlg.timesheet.date: wlg.hours for wlg in groups}

    @staticmethod
    def _get_day_ranges(owner):
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
    def _get_forecast_hours(days, employee, start_date, end_date):
        """
        Get the total estimated hours per day for the given employee.
        """
        day_type_hours = {sh.day_type: sh.hours for sh in
                          StandardHours.objects.for_owner(employee.owner)}
        res = {}
        for day in days:
            h = day_type_hours.get(day.type)
            if h:
                res[day.date] = h
        return res

    @staticmethod
    def _split_hours_per_type(hours, ranges):
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
    def _get_adjusted_hours(cls, period, employee):
        """
        Get a dictionary of
        """
        sql = '''SELECT
        pf.id AS id, pf.period_id, pf.phase, pf.employee_id, pf.hour_type_id, COALESCE(pr.hours, 0) - pf.hours AS hours
        FROM (SELECT * from payroll_workedhours WHERE phase = %s AND period_id = %s AND employee_id = %s)
        as pf
        LEFT OUTER JOIN (SELECT * from payroll_workedhours WHERE phase = %s and period_id = %s AND employee_id = %s)
        as pr
        ON (pf.hour_type_id = pr.hour_type_id)
        '''
        params = [cls.PHASE_FORECAST, period.previous.id, employee.id,
                  cls.PHASE_RETROACTIVE, period.previous.id, employee.id]
        return {wh.hour_type: wh.hours for wh in cls.objects.raw(sql, params)}

    @classmethod
    def calculate(cls, period, phase, employee):
        """
        Get new WorkedHours instances for the given period, employee and phase.
        """
        if phase == cls.PHASE_ADJUSTMENT:
            hours_per_type = cls._get_adjusted_hours(period, employee)

        else:
            if phase == cls.PHASE_FORECAST:
                # Forecast phase
                start = period.forecast_start_date
                end = period.end_date
                hours_method = cls._get_forecast_hours

            else:
                if phase == cls.PHASE_ACTUAL:
                    start = period.start_date
                    end = period.forecast_start_date - timedelta(days=1)
                else:
                    start = period.forecast_start_date
                    end = period.end_date
                hours_method = cls._get_actual_hours

            # Now get days, ranges and hours per day
            days = CalendarDay.objects.in_range(start, end)
            ranges = cls._get_day_ranges(employee.owner)
            daily_hours = hours_method(days, employee, start, end)

            # Now calculate the types
            hours_per_type = {}
            for day in days:
                hpt = cls._split_hours_per_type(daily_hours.get(day.date, 0), ranges[day.type])
                for ht, h in hpt.items():
                    hours_per_type[ht] = hours_per_type.get(ht, 0) + h

        # Now return the list, one per type:hours
        return [cls(employee=employee, period=period, phase=phase,
                    hour_type=ht, hours=h)
                for ht, h in hours_per_type.items()]

