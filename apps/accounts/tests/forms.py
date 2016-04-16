
from django.test import TestCase

from ..forms import UserForm
from ..models import User
from ..factories import UserFakeFactory
from ..utils import ensure_permissions


class UserFormTest(TestCase):

    def test_save_owner(self):
        # Create admin user that can add users
        admin = UserFakeFactory.create()
        admin.user_permissions.add(*ensure_permissions(User, ['add']))

        # Render and submit the form
        form = UserForm({'username': 'karina', 'password': '123'}, user=admin)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that new user was created with correct owner
        karina = User.objects.latest('date_joined')
        self.assertEqual(karina.username, 'karina@{}'.format(admin.owner.code))
        self.assertEqual(karina.owner, admin.owner)
