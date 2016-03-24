__author__ = 'claudio.melendrez'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...deployment.factories import TimeSheetFactory
from ...deployment.models import TimeSheet


class TimeSheetViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.ts = TimeSheetFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon entry, not allowed
        res = self.client.get(reverse('timesheets'))
        self.assertEqual(res.status_code, 401)

        # Login, OK
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('timesheets'))
        self.assertEqual(res.status_code, 200)

        # View detail, OK
        res = self.client.get(reverse('timesheet', kwargs={'pk': self.ts.id}))
        self.assertEqual(res.status_code, 200)

        # Attempt to access add view, not allowed
        res = self.client.get(reverse('timesheet', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission, now access add view ok
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['add']))
        res = self.client.get(reverse('timesheet', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Attempt to access edit view, not allowed
        res = self.client.get(reverse('timesheet', kwargs={'pk': self.ts.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission, now access edit view ok
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['change']))
        res = self.client.get(reverse('timesheet', kwargs={'pk': self.ts.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class TimeSheetActionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.ts = TimeSheetFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon entry, not allowed
        res = self.client.get(reverse('timesheet-action', kwargs={'pk': self.ts.id}))
        self.assertEqual(res.status_code, 401)

        # Login, still not allowed
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('timesheet-action', kwargs={'pk': self.ts.id}))
        self.assertEqual(res.status_code, 403)

        # View detail, OK
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['issue']))
        res = self.client.get(reverse('timesheet-action', kwargs={'pk': self.ts.id}))
        self.assertEqual(res.status_code, 200)


class HoursViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')

    def test_get(self):
        # Anon entry, not allowed
        res = self.client.get(reverse('hours'))
        self.assertEqual(res.status_code, 401)

        # Login, OK
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('hours'))
        self.assertEqual(res.status_code, 200)
