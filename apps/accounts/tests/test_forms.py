
from django.test import TestCase

from ..forms import UserForm
from ..models import User
from ..factories import UserFactory
from ..utils import create_permissions


class UserFormTest(TestCase):

    def test_save_owner(self):
        # Create admin user that can add users
        admin = UserFactory.create()
        admin.user_permissions.add(*create_permissions(User, ['add']))

        # Render and submit the form
        form = UserForm({'username': 'Karina'}, user=admin)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that new user was created with correct owner
        karina = User.objects.latest('date_joined')
        self.assertEqual(karina.username, 'Karina')
        self.assertEqual(karina.owner, admin.owner)
