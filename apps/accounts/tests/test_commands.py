__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ..models import Account, User


class CreteExampleAccountTest(TestCase):

    def test_create_example_account(self):
        n_accounts = Account.objects.count()
        n_users = User.objects.count()

        # Call command
        call_command('create_example_account')

        # Check number of accounts and users added
        self.assertEqual(Account.objects.count(), n_accounts + 1)
        self.assertEqual(User.objects.count(), n_users + 7)

        # Check their data
        acc = Account.objects.last()
        self.assertEqual(User.objects.filter(owner=acc).count(), 7)
        u1, u2, u3, u4, u5, u6, u7 = User.objects.all()[n_users:]
        self.assertEqual(u1.groups.all()[0].name, 'Administrators')
        self.assertEqual(u2.groups.all()[0].name, 'Human Resources')
        self.assertEqual(u3.groups.all()[0].name, 'Team Management')
        self.assertEqual(u4.groups.all()[0].name, 'Project Control')
        self.assertEqual(u5.groups.all()[0].name, 'Project Management')
        self.assertEqual(u6.groups.all()[0].name, 'Time-Keeping')
        self.assertEqual(u7.groups.all()[0].name, 'Supervision')
