__author__ = 'kako'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ..factories import PeriodFactory
from ..models import WorkedHours


class WorkedHoursViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create user and period
        self.user = UserFactory.create(password='123')
        self.period = PeriodFactory.create(owner=self.user.owner)

    def test_view(self):
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id})

        # Anon use, auth error
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

        # Logged user, can view OK
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # Attempt to access payroll process view, not authorized
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

        # Add permission to do it, should view it now
        self.user.user_permissions.add(*create_permissions(WorkedHours, ['add']))
        url = reverse('worked-hours', kwargs={'period_pk': self.period.id, 'action': 'process'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
