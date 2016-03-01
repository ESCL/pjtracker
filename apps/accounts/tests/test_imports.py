__author__ = 'kako'

from django.test import TestCase

from ..factories import AccountFactory, UserFactory
from ..models import Account, User


class UserFactoryTestCase(TestCase):

    def setUp(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        self.account1 = AccountFactory.create()
        self.account2 = AccountFactory.create()

    def test_get_or_create(self):
        # Create a user with x data
        row = {'username': 'peter', 'owner': self.account1}
        user1 = UserFactory.create(**row)
        self.assertEqual(User.objects.count(), 1)

        # Attempt creation with similar data, should not create a new one
        user2 = UserFactory.create(**row)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user1, user2)

        # Change owner, should create it now
        row['owner'] = self.account2
        user3 = UserFactory.create(**row)
        self.assertEqual(User.objects.count(), 2)
        self.assertNotEqual(user1, user3)


class UserImportTestCase(TestCase):

    def setUp(self):
        self.skipTest('')