
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

        # Create user to modify
        # Note: end-users cannot add users (yet?)
        karina = UserFakeFactory.create(owner=admin.owner)
        self.assertEqual(karina.email, '')

        # Render and submit the form
        form = UserForm({'username': 'karina', 'email': 'karina@gmail.com'},
                        user=admin, instance=karina)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that new user was created with correct owner
        karina = User.objects.get(id=karina.id)
        self.assertEqual(karina.username, 'karina@{}'.format(admin.owner.code))
        self.assertEqual(karina.email, 'karina@gmail.com')
