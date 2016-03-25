__author__ = 'kako'

from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...deployment.models import WorkLog
from ...resources.factories import EmployeeFactory
from ..factories import PeriodFactory, NormalHoursFactory, Overtime150HoursFactory, Overtime200HoursFactory
from ..models import WorkedHours, HourType, HourTypeRange, CalendarDay, Period


class CalendarDayViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.cd = CalendarDay(owner=self.user.owner,
                              date=date(2015, 10, 21), name='Kako BD 30')
        self.cd.save()

    def test_get(self):
        # Anon user tried to view calendar, not authenticated
        res = self.client.get(reverse('calendar'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view calendar
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('calendar'))
        self.assertEqual(res.status_code, 200)

        # View calendar day, ok
        res = self.client.get(reverse('calendar-day', kwargs={'pk': self.cd.id}))
        self.assertEqual(res.status_code, 200)

        # Try to add one, nope
        res = self.client.get(reverse('calendar-day', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give access to add, can now add
        self.user.user_permissions.add(*create_permissions(CalendarDay, ['add']))
        res = self.client.get(reverse('calendar-day', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Try to edit one, nope
        res = self.client.get(reverse('calendar-day', kwargs={'action': 'edit', 'pk': self.cd.id}))
        self.assertEqual(res.status_code, 403)

        # Give access to edit, can edit ok
        self.user.user_permissions.add(*create_permissions(CalendarDay, ['change']))
        res = self.client.get(reverse('calendar-day', kwargs={'action': 'edit', 'pk': self.cd.id}))
        self.assertEqual(res.status_code, 200)


class HourTypeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.ht = NormalHoursFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user tried to view calendar, not authenticated
        res = self.client.get(reverse('hour-types'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view calendar
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('hour-types'))
        self.assertEqual(res.status_code, 200)

        # View calendar day, ok
        res = self.client.get(reverse('hour-type', kwargs={'pk': self.ht.id}))
        self.assertEqual(res.status_code, 200)

        # Try to add one, nope
        res = self.client.get(reverse('hour-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give access to add, can now add
        self.user.user_permissions.add(*create_permissions(HourType, ['add']))
        res = self.client.get(reverse('hour-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Try to edit one, nope
        res = self.client.get(reverse('hour-type', kwargs={'action': 'edit', 'pk': self.ht.id}))
        self.assertEqual(res.status_code, 403)

        # Give access to edit, can edit ok
        self.user.user_permissions.add(*create_permissions(HourType, ['change']))
        res = self.client.get(reverse('hour-type', kwargs={'action': 'edit', 'pk': self.ht.id}))
        self.assertEqual(res.status_code, 200)


class PeriodViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.period = PeriodFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user tried to view calendar, not authenticated
        res = self.client.get(reverse('periods'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view calendar
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('periods'))
        self.assertEqual(res.status_code, 200)

        # View calendar day, ok
        res = self.client.get(reverse('period', kwargs={'pk': self.period.id}))
        self.assertEqual(res.status_code, 200)

        # Try to add one, nope
        res = self.client.get(reverse('period', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give access to add, can now add
        self.user.user_permissions.add(*create_permissions(Period, ['add']))
        res = self.client.get(reverse('period', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Try to edit one, nope
        res = self.client.get(reverse('period', kwargs={'action': 'edit', 'pk': self.period.id}))
        self.assertEqual(res.status_code, 403)

        # Give access to edit, can edit ok
        self.user.user_permissions.add(*create_permissions(Period, ['change']))
        res = self.client.get(reverse('period', kwargs={'action': 'edit', 'pk': self.period.id}))
        self.assertEqual(res.status_code, 200)


class WorkedHoursViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create user and period (as previous to work with adjustment)
        self.user = UserFactory.create(password='123')
        self.period = PeriodFactory.create(owner=self.user.owner)
        PeriodFactory.create(owner=self.user.owner, end_date=self.period.start_date - timedelta(days=1))

        # Set hour types and their ranges
        self.std = NormalHoursFactory.create(owner=self.period.owner)
        self.ot150 = Overtime150HoursFactory.create(owner=self.period.owner)
        self.ot200 = Overtime200HoursFactory.create(owner=self.period.owner)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.WEEKDAY, hour_type=self.std, limit=8)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.WEEKDAY, hour_type=self.ot150)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SATURDAY, hour_type=self.ot150, limit=4)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SATURDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.SUNDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(owner=self.period.owner, day_type=CalendarDay.PUBLIC_HOLIDAY, hour_type=self.ot200)

        # Clear worklogs, just in case
        WorkLog.objects.all().delete()

        # Nor create employee with a few processed hours
        self.e = EmployeeFactory.create(owner=self.period.owner)
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
        self.user.user_permissions.add(*create_permissions(WorkedHours, ['add']))
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_process(self):
        # Give permissions and login
        self.user.user_permissions.add(*create_permissions(WorkedHours, ['add']))
        self.client.login(username=self.user.username, password='123')

        # Check that setUp worked hours are there
        self.assertEqual(WorkedHours.objects.filter(period=self.period).count(), 6)

        # Now process period again
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        self.client.post(url, data={'confirm': 'yes'})

        # Should have removed everything (since there are no work logs)
        self.assertEqual(WorkedHours.objects.filter(period=self.period).count(), 0)
