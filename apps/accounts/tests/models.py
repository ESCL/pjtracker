
from django.test import TestCase

from ..models import Account, User
from ..factories import UserFakeFactory
from ..utils import ensure_permissions


class UserTest(TestCase):

    def test_user_filter(self):
        # Create three users with two different accounts
        user1 = UserFakeFactory.create(password='123')
        user2 = UserFakeFactory.create(password='123')
        user3 = UserFakeFactory.create(owner=user2.owner, password='123')

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
        user = UserFakeFactory.create(password='123')
        user.user_permissions.add(*ensure_permissions(User, ['add', 'change']))

        # Actions should be simple
        actions = user.get_allowed_actions_for(User)
        self.assertEqual(set(actions), {('add',), ('change',)})

        # Create one that can only change usernames
        user = UserFakeFactory.create(password='123')
        user.user_permissions.add(*ensure_permissions(User, ['change username']))

        # Actions should include field name
        actions = user.get_allowed_actions_for(User)
        self.assertEqual(actions, [('change', 'username')])

    def test_get_disallowed_fields(self):
        # Create an admin that can change anything
        user = UserFakeFactory.create(password='123')
        user.user_permissions.add(*ensure_permissions(User, ['add', 'change']))

        # Actions should be simple
        fields = user.get_disallowed_fields_for(User(owner=user.owner))
        self.assertEqual(fields, set())

        # Create one that can only change usernames
        user = UserFakeFactory.create(password='123')
        user.user_permissions.add(*ensure_permissions(User, ['change username']))

        # Check fields, only username is removed
        fields = user.get_disallowed_fields_for(User(owner=user.owner))
        self.assertEqual(fields, set(User._meta.get_all_field_names()).difference({'username'}))

    def test_username(self):
        # Create user (with account)
        user = UserFakeFactory.create(password='123')
        self.assertIsNotNone(user.owner)

        # Check username includes @<account.code>
        self.assertTrue('@{}'.format(user.owner.code) in user.username)

        # Remove account, username now excludes account code
        user.owner = None
        user.save()
        self.assertFalse('@' in user.username)

    def test_query_domain(self):
        User.objects.all().delete()

        # Add one global user and two for an account
        staff = UserFakeFactory.create(owner=None, password='123')
        acc_admin = UserFakeFactory.create(password='123')
        acc_user = UserFakeFactory.create(owner=acc_admin.owner, password='123')

        # Staff gets list, all are there
        qs = User.objects.for_user(staff)
        self.assertEqual(qs.count(), 3)
        self.assertEqual(set(qs), {staff, acc_admin, acc_user})

        # Account admin gets list, staff is not there
        qs = User.objects.for_user(acc_admin)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(set(qs), {acc_admin, acc_user})
