from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...common.test import mock
from ...deployment.models import TimeSheetSettings, TimeSheet
from ..factories import UserFactory
from ..models import User
from ..utils import create_permissions


class AuthViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
        self.skipTest('')

    def test_logout(self):
        self.skipTest('')


class SettingsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Note: set password to avoid bug (https://github.com/ESCL/pjtracker/issues/40)
        self.user = UserFactory.create(password='123')
        self.url = reverse('settings')

    def test_view(self):
        # Anonymous user, not authenticated
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 401)

        # Logged in user, but not authorized
        self.assertTrue(self.client.login(username=self.user.username, password='123'))
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 403)

        # Add authorization, now user should be able to view
        self.user.user_permissions.add(*create_permissions(TimeSheetSettings, ['change']))
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    @mock.patch('apps.deployment.forms.TimeSheetSettingsForm.save')
    @mock.patch('apps.payroll.forms.HoursSettingsForm.save')
    def test_post(self, hsf_save, tssf_save):
        # Anonymous user, not authenticated
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, 401)

        # Logged in user, but not authorized
        self.assertTrue(self.client.login(username=self.user.username, password='123'))
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, 403)

        # Invalid data
        self.user.user_permissions.add(*create_permissions(TimeSheetSettings, ['change']))
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(hsf_save.called)
        self.assertFalse(tssf_save.called)

        # Now post valid data, should have saved forms
        # Note: hours settings form is empty, save is no-op but still called
        data = {'approval_policy': TimeSheet.REVIEW_POLICY_ALL,
                'rejection_policy': TimeSheet.REVIEW_POLICY_FIRST}
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(hsf_save.called)
        self.assertTrue(tssf_save.called)


class UserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Note: set password to avoid bug (https://github.com/ESCL/pjtracker/issues/40)
        self.user = UserFactory.create(password='123')

    def test_view(self):
        url = reverse('users')

        # Anonymous user, not authenticated
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

        # Logged in user, cannot see
        self.assertTrue(self.client.login(username=self.user.username, password='123'))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # View user detail, OK
        url = reverse('user', kwargs={'pk': self.user.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # Edit user, no access
        url = reverse('user', kwargs={'pk': self.user.id, 'action': 'edit'})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

        # Make it account admin
        self.user.user_permissions.add(*create_permissions(User, ['add', 'change']))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
