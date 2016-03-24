__author__ = 'claudio.melendrez'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ..factories import CompanyFactory, PositionFactory, TeamFactory
from ..models import Company, Position, Team


class CompanyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.company = CompanyFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon view tries to view list, not allowed
        res = self.client.get(reverse('companies'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('companies'))
        self.assertEqual(res.status_code, 200)

        # It can also view details
        res = self.client.get(reverse('company', kwargs={'pk': self.company.id}))
        self.assertEqual(res.status_code, 200)

        # But it cannot add one
        res = self.client.get(reverse('company', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give permission to add, now it can
        self.user.user_permissions.add(*create_permissions(Company, ['add']))
        res = self.client.get(reverse('company', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # But it cannot edit
        res = self.client.get(reverse('company', kwargs={'pk': self.company.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, now it can
        self.user.user_permissions.add(*create_permissions(Company, ['change']))
        res = self.client.get(reverse('company', kwargs={'pk': self.company.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class PositionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.position = PositionFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon view tries to view list, not allowed
        res = self.client.get(reverse('positions'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('positions'))
        self.assertEqual(res.status_code, 200)

        # It can also view details
        res = self.client.get(reverse('position', kwargs={'pk': self.position.id}))
        self.assertEqual(res.status_code, 200)

        # But it cannot add one
        res = self.client.get(reverse('position', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give permission to add, now it can
        self.user.user_permissions.add(*create_permissions(Position, ['add']))
        res = self.client.get(reverse('position', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # But it cannot edit
        res = self.client.get(reverse('position', kwargs={'pk': self.position.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit labour types, now it can
        self.user.user_permissions.add(*create_permissions(Position, ['change labour types']))
        res = self.client.get(reverse('position', kwargs={'pk': self.position.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class TeamViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.team = TeamFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon view tries to view list, not allowed
        res = self.client.get(reverse('teams'))
        self.assertEqual(res.status_code, 401)

        # Login, now it can view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('teams'))
        self.assertEqual(res.status_code, 200)

        # It can also view details
        res = self.client.get(reverse('team', kwargs={'pk': self.team.id}))
        self.assertEqual(res.status_code, 200)

        # But it cannot add one
        res = self.client.get(reverse('team', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Give permission to add, now it can
        self.user.user_permissions.add(*create_permissions(Team, ['add']))
        res = self.client.get(reverse('team', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # But it cannot edit
        res = self.client.get(reverse('team', kwargs={'pk': self.team.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit team activities, now it can
        self.user.user_permissions.add(*create_permissions(Team, ['change activities']))
        res = self.client.get(reverse('team', kwargs={'pk': self.team.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)
