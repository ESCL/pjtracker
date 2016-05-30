__author__ = 'kako'

from datetime import timedelta

from django_group_by import GroupByMixin

from ..common.db.query import OwnedEntityQuerySet
from ..common.exceptions import InvalidOperationError


class CalendarDayQuerySet(OwnedEntityQuerySet):

    def in_range(self, cur_date, end_date):
        """
        Get a list of CalendarDays, stored or not.
        """
        # Start with all the stored ones
        res = {cd.date: cd for cd in self.filter(date__gte=cur_date, date__lte=end_date)}

        # Add one for each
        while cur_date <= end_date:
            if cur_date not in res:
                cd = self.model(date=cur_date)
                res[cur_date] = cd
            cur_date += timedelta(days=1)

        return sorted(res.values())


class WorkedHoursQuerySet(OwnedEntityQuerySet, GroupByMixin):

    def create(self, **kwargs):
        """
        Disable creation of instances through queryset, since only saving
        initialized instances is allowed.

        :param kwargs: instance field values
        :raise: InvalidOperationError
        """
        raise InvalidOperationError('Creating {} instances from queryset is '
                                    'not allowed.'.format(self.model.__name__))

    def for_payroll(self, period):
        """
        Filter the phases that are make up the "payroll subtotals", eg.
        adjustment, actual and forecast.

        Note: usually retroactive would not be calculated yet

        :return: filtered queryset
        """
        payroll_phases = (self.model.PHASE_ADJUSTMENT,
                          self.model.PHASE_ACTUAL,
                          self.model.PHASE_FORECAST)
        return self.filter(period=period, phase__in=payroll_phases)

    def consolidated(self):
        """
        Yield dictionaries with the joined worked hours per type for each
        employee for the queryset.

        Note: this operation is final and the result cannot be.
        """
        # Start with empty dict
        d = {}

        # Iterate results
        for wh in self.order_by('employee'):
            if d.get('employee') != wh.employee:
                # New or different employee
                if d:
                    # Different employee, yield the previous one
                    yield d
                # Reset dict
                d = {'employee': wh.employee, 'total': 0}

            # Add worked hours in dict
            if wh.hour_type.code not in d:
                d[wh.hour_type.code] = 0
            d[wh.hour_type.code] += wh.hours
            d['total'] += wh.hours

        # Finally, yield the last one
        yield d
