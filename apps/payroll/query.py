__author__ = 'kako'

from datetime import timedelta

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


class WorkedHoursQuerySet(OwnedEntityQuerySet):

    def create(self, **kwargs):
        """
        Disable creation of instances through queryset, since only saving
        initialized instances is allowed.

        :param kwargs: instance field values
        :raise: InvalidOperationError
        """
        raise InvalidOperationError('Creating {} instances from queryset is '
                                    'not allowed.'.format(self.model.__name__))
