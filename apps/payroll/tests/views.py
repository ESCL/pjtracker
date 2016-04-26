__author__ = 'kako'

from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...common.test import PermissionTestMixin
from ...accounts.factories import UserFakeFactory
from ...accounts.utils import ensure_permissions
from ...deployment.models import WorkLog
from ...resources.factories import EmployeeFakeFactory
from ..factories import (CalendarDayFakeFactory, PeriodFakeFactory, NormalHoursFakeFactory,
                         Overtime150HoursFakeFactory, Overtime200HoursFakeFactory)
from ..models import WorkedHours, HourType, HourTypeRange, CalendarDay, Period


class CalendarDayViewTest(PermissionTestMixin, TestCase):
    model = CalendarDay
    model_factory = CalendarDayFakeFactory
    list_view_name = 'calendar'
    instance_view_name = 'calendar-day'


class HourTypeViewTest(PermissionTestMixin, TestCase):
    model = HourType
    model_factory = NormalHoursFakeFactory
    list_view_name = 'hour-types'
    instance_view_name = 'hour-type'


class PeriodViewTest(PermissionTestMixin, TestCase):
    model = Period
    model_factory = PeriodFakeFactory
    list_view_name = 'periods'
    instance_view_name = 'period'


class WorkedHoursViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create user and period (as previous to work with adjustment)
        self.user = UserFakeFactory.create(password='123')
        self.period = PeriodFakeFactory.create(owner=self.user.owner)
        PeriodFakeFactory.create(owner=self.user.owner, end_date=self.period.start_date - timedelta(days=1))

        # Set hour types and their ranges
        self.std = NormalHoursFakeFactory.create(owner=self.period.owner)
        self.ot150 = Overtime150HoursFakeFactory.create(owner=self.period.owner)
        self.ot200 = Overtime200HoursFakeFactory.create(owner=self.period.owner)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.WEEKDAY, hour_type=self.std, limit=8)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.WEEKDAY, hour_type=self.ot150)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SATURDAY, hour_type=self.ot150, limit=4)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SATURDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SUNDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.PUBLIC_HOLIDAY, hour_type=self.ot200)

        # Clear worklogs, just in case
        WorkLog.objects.all().delete()

        # Nor create employee with a few processed hours
        self.e = EmployeeFakeFactory.create(owner=self.period.owner)
        d = {'owner': self.period.owner, 'period': self.period, 'employee': self.e}
        WorkedHours(phase=WorkedHours.PHASE_ADJUSTMENT, hour_type=self.std, hours=-15, **d).save()
        WorkedHours(phase=WorkedHours.PHASE_ADJUSTMENT, hour_type=self.ot150, hours=-4, **d).save()
        WorkedHours(phase=WorkedHours.PHASE_ACTUAL, hour_type=self.std, hours=160, **d).save()
        WorkedHours(phase=WorkedHours.PHASE_ACTUAL, hour_type=self.ot150, hours=10, **d).save()
        WorkedHours(phase=WorkedHours.PHASE_ACTUAL, hour_type=self.ot200, hours=6, **d).save()
        WorkedHours(phase=WorkedHours.PHASE_FORECAST, hour_type=self.std, hours=56, **d).save()

    def test_view(self):
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id})

        # Anon use, auth error
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

        # Logged user, can view OK
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.e.full_name)

        # Attempt to access payroll process view, not authorized
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

        # Add permission to do it, should view it now
        self.user.user_permissions.add(*ensure_permissions(WorkedHours, ['add']))
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_process(self):
        # Give permissions and login
        self.user.user_permissions.add(*ensure_permissions(WorkedHours, ['add']))
        self.client.login(username=self.user.username, password='123')

        # Check that setUp worked hours are there
        self.assertEqual(WorkedHours.objects.filter(period=self.period).count(), 6)

        # Now process period again
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        self.client.post(url, data={'confirm': 'yes'})

        # Should have removed everything (since there are no work logs)
        self.assertEqual(WorkedHours.objects.filter(period=self.period).count(), 0)
