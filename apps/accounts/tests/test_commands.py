__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ..models import Account, User


class CreteExampleAccountTest(TestCase):

    def tearDown(self):
        # Delete account and its objects
        self.account.delete()

    def test_create_example_account(self):
        # Call command
        call_command('create_example_account')

        # Check number of accounts and users added
        self.account = Account.objects.last()
        users = User.objects.filter(owner=self.account)
        self.assertEqual(users.count(), 7)

        # Check the users' groups (one of each)
        u1, u2, u3, u4, u5, u6, u7 = users
        self.assertEqual(u1.groups.all()[0].name, 'Administrators')
        self.assertEqual(u2.groups.all()[0].name, 'Human Resources')
        self.assertEqual(u3.groups.all()[0].name, 'Team Management')
        self.assertEqual(u4.groups.all()[0].name, 'Project Control')
        self.assertEqual(u5.groups.all()[0].name, 'Project Management')
        self.assertEqual(u6.groups.all()[0].name, 'Time-Keeping')
        self.assertEqual(u7.groups.all()[0].name, 'Supervision')
