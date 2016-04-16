
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import ensure_permissions
from ..factories import LocationFactory
from ..models import Location


class LabourTypeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.location = LocationFactory.create()

    def test_get(self):
        # Anon user, cannot view list of labour types
        res = self.client.get(reverse('locations'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of labour types
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('locations'))
        self.assertEqual(res.status_code, 200)

        # And also individual labour type
        res = self.client.get(reverse('location', kwargs={'pk': self.location.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add labour type
        res = self.client.get(reverse('location', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add labour type
        self.user.user_permissions.add(*ensure_permissions(Location, ['add']))
        res = self.client.get(reverse('location', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit labour type
        res = self.client.get(reverse('location', kwargs={'pk': self.location.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit labour type
        self.user.user_permissions.add(*ensure_permissions(Location, ['change']))
        res = self.client.get(reverse('location', kwargs={'pk': self.location.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)
