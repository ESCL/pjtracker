__author__ = 'claudio.melendrez'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...common.test import PermissionTestMixin
from ...accounts.factories import UserFactory
from ...accounts.utils import ensure_permissions
from ...deployment.factories import TimeSheetFactory
from ...deployment.models import TimeSheet


class TimeSheetViewTest(PermissionTestMixin, TestCase):
    model = TimeSheet
    model_factory = TimeSheetFactory
    list_view_name = 'timesheets'
    instance_view_name = 'timesheet'


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
        self.user.user_permissions.add(*ensure_permissions(TimeSheet, ['issue']))
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
