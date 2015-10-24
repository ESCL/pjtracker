
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Account, UserProfile
from .factories import AccountFactory, UserFactory, UserProfileFactory


class UserProfileTest(TestCase):

    def test_user_factory(self):
        # Just testing the behaviour
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

        # Create a user, should add a profile and and account
        user = UserFactory.create()
        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.profile.account)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

