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




class HourTypeRange(OwnedEntity):

    class Meta:
        ordering = ('day_type', 'limit',)

    day_type = models.CharField(
        max_length=3,
        choices=((CalendarDay.WEEKDAY, 'Weekday'),
                 (CalendarDay.SATURDAY, 'Saturday'),
                 (CalendarDay.SUNDAY, 'Sunday'),
                 (CalendarDay.PUBLIC_HOLIDAY, 'Public Holiday'),
                 (CalendarDay.NATIONAL_HOLIDAY, 'National Holiday'),
                 (CalendarDay.STATE_HOLIDAY, 'State Holiday'))
    )
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
    predicted_days = models.PositiveIntegerField(
    )

    def save(self, *args, **kwargs):
        self.code = '{:%Y-%m}'.format(self.start_date)
        if not self.name:
            self.name = '{:%b %Y}'.format(self.start_date)

        return super(Period, self).save(*args, **kwargs)


class WorkedHours(OwnedEntity):

    SOURCE_ACTUAL = 'A'
    SOURCE_PREDICTED = 'P'
    ENACTMENT_CURRENT = 'C'
    ENACTMENT_RETROACTIVE = 'R'

    period = models.ForeignKey(
        'Period'
    )
    source = models.CharField(
        max_length=1,
        db_index=True,
        choices=((SOURCE_ACTUAL, 'Actual'),
                 (SOURCE_PREDICTED, 'Predicted'))
    )
    enactment = models.CharField(
        max_length=1,
        db_index=True,
        choices=((ENACTMENT_CURRENT, 'Current'),
                 (ENACTMENT_RETROACTIVE, 'Retroactive'))
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

    @classmethod
    def calculate_actual(cls, period, employee, enactment):
        # Get hour type ranges per day type
        day_ranges = {}
        for range in HourTypeRange.objects.for_owner(period.owner):
            if range.day_type not in day_ranges:
                day_ranges[range.day_type] = []
            day_ranges[range.day_type].append(range)

        # Determine the dates
        if enactment == cls.ENACTMENT_CURRENT:
            start_date = period.start_date
            end_date = period.end_date - timedelta(days=period.predicted_days)
        else:
            start_date = period.end_date - timedelta(days=period.predicted_days + 1)
            end_date = period.end_date

        # Get all the days in the range (stored or not)
        days = CalendarDay.objects.in_range(start_date, end_date)

        # Get the work logs
        groups = WorkLog.objects.filter(
            resource=employee.resource_ptr,
            timesheet__status=TimeSheet.STATUS_APPROVED,
            timesheet__date__gte=start_date,
            timesheet__date__lte=end_date
        )

        # Now collect hours per hour type
        hour_per_type = {}
        for wlg in groups.values('timesheet__date').annotate(hours=models.Sum('hours')):
            day = days[wlg.timesheet.date]
            cur_limit = 0

            for r in day_ranges[day.type]:
                # Get hours, sliced to respect both limits
                h = min(max(wlg.hours - cur_limit, 0), r.limit)

                if h:
                    # Hours are not zero, add them
                    if r.hour_type not in hour_per_type:
                        hour_per_type[r.hour_type] = 0
                    hour_per_type[r.hour_type] += h

                # Update limit for next one
                cur_limit = r.limit or 0

        return [cls(employee=employee, period=period, source=cls.SOURCE_ACTUAL,
                    enactment=enactment, hour_type=ht, hours=h)
                for ht, h in hour_per_type.items()]
