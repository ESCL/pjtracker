__author__ = 'claudio.melendrez'

from ..factories import AccountFakeFactory, UserFakeFactory
from ..models import Account, User

from django.test import TestCase


class UserFactoryTest(TestCase):

    def setUp(self):
        User.objects.all().delete()
        Account.objects.all().delete()

    def test_create(self):
        # Just testing the behaviour
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)

        # Create a user, should add a profile and an account
        user = UserFakeFactory.create(password='123')
        self.assertIsNotNone(user.owner)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)

        # Account should also add settings through signals
        self.assertIsNotNone(user.owner.timesheet_settings)

    def test_get_or_create(self):
        account1 = AccountFakeFactory.create()
        account2 = AccountFakeFactory.create()

        # Create a user with x data
        row = {'username': 'peter', 'owner': account1}
        user1 = UserFakeFactory.create(**row)
        self.assertEqual(User.objects.count(), 1)

        # Attempt creation with similar data, should not create a new one
        user2 = UserFakeFactory.create(**row)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user1, user2)

        # Change owner, should create it now
        row['owner'] = account2
        user3 = UserFakeFactory.create(**row)
        self.assertEqual(User.objects.count(), 2)
        self.assertNotEqual(user1, user3)
