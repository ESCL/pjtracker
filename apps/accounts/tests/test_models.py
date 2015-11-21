
from django.test import TestCase

from ..models import Account, User
from ..factories import UserFactory
from ..utils import create_permissions


class UserTest(TestCase):

    def test_user_factory(self):
        # Just testing the behaviour
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)

        # Create a user, should add a profile and and account
        user = UserFactory.create()
        self.assertIsNotNone(user.owner)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)

        # Account should also add settings through signals
        self.assertIsNotNone(user.owner.timesheet_settings)

    def test_user_filter(self):
        # Create three users with two different accounts
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create(owner=user2.owner)

        # Make sure they have different accounts
        self.assertNotEqual(user1.owner, user2.owner)

        # Check that user1 can only see himself
        qs = User.objects.for_user(user1)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], user1)

        # Check that user2 can only see himself and his partner
        qs = User.objects.for_user(user2)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], user2)
        self.assertEqual(qs[1], user3)

    def test_get_allowed_actions(self):
        # Create an admin that can change anything
        user = UserFactory.create()
        user.user_permissions.add(*create_permissions(User, ['add', 'change']))

        # Actions should be simple
        actions = user.get_allowed_actions_for(User)
        self.assertEqual(set(actions), {('add',), ('change',)})

        # Create one that can only change usernames
        user = UserFactory.create()
        user.user_permissions.add(*create_permissions(User, ['change username']))

        # Actions should include field name
        actions = user.get_allowed_actions_for(User)
        self.assertEqual(actions, [('change', 'username')])

    def test_get_disallowed_fields(self):
        # Create an admin that can change anything
        user = UserFactory.create()
        user.user_permissions.add(*create_permissions(User, ['add', 'change']))

        # Actions should be simple
        fields = user.get_disallowed_fields_for(User(owner=user.owner))
        self.assertEqual(fields, set())

        # Create one that can only change usernames
        user = UserFactory.create()
        user.user_permissions.add(*create_permissions(User, ['change username']))

        # Check fields, only username is removed
        fields = user.get_disallowed_fields_for(User(owner=user.owner))
        self.assertEqual(fields, set(User._meta.get_all_field_names()).difference({'username'}))
