__author__ = 'kako'

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ...accounts.factories import UserFactory
from ...accounts.utils import ensure_permissions
from ..factories import EmployeeFactory, EquipmentFactory, EquipmentTypeFactory
from ..models import Employee, Equipment, EquipmentType


class EmployeeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.e = EmployeeFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user, cannot view list of employees
        res = self.client.get(reverse('employees'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('employees'))
        self.assertEqual(res.status_code, 200)

        # View individual employee, OK
        res = self.client.get(reverse('employee', kwargs={'pk': self.e.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add an employee
        res = self.client.get(reverse('employee', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add employees, OK now
        self.user.user_permissions.add(*ensure_permissions(Employee, ['add']))
        res = self.client.get(reverse('employee', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Attempt to edit employee, nope
        res = self.client.get(reverse('employee', kwargs={'pk': self.e.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, OK now
        self.user.user_permissions.add(*ensure_permissions(Employee, ['change']))
        res = self.client.get(reverse('employee', kwargs={'pk': self.e.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class EquipmentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.e = EquipmentFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user, cannot view list of equipment
        res = self.client.get(reverse('equipments'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('equipments'))
        self.assertEqual(res.status_code, 200)

        # And can view individual equipment
        res = self.client.get(reverse('equipment', kwargs={'pk': self.e.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add an equipment
        res = self.client.get(reverse('equipment', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, now user can add equipment
        self.user.user_permissions.add(*ensure_permissions(Equipment, ['add']))
        res = self.client.get(reverse('equipment', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # Attempt to edit equipment, nope
        res = self.client.get(reverse('equipment', kwargs={'pk': self.e.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit equipment
        self.user.user_permissions.add(*ensure_permissions(Equipment, ['change']))
        res = self.client.get(reverse('equipment', kwargs={'pk': self.e.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)


class EquipmentTypeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(password='123')
        self.et = EquipmentTypeFactory.create(owner=self.user.owner)

    def test_get(self):
        # Anon user, cannot view list of types
        res = self.client.get(reverse('equipment-types'))
        self.assertEqual(res.status_code, 401)

        # Login, user can now view list of types
        self.client.login(username=self.user.username, password='123')
        res = self.client.get(reverse('equipment-types'))
        self.assertEqual(res.status_code, 200)

        # And also individual type
        res = self.client.get(reverse('equipment-type', kwargs={'pk': self.et.id}))
        self.assertEqual(res.status_code, 200)

        # User cannot add type
        res = self.client.get(reverse('equipment-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to add, user can now add type
        self.user.user_permissions.add(*ensure_permissions(EquipmentType, ['add']))
        res = self.client.get(reverse('equipment-type', kwargs={'action': 'add'}))
        self.assertEqual(res.status_code, 200)

        # User cannot edit type
        res = self.client.get(reverse('equipment-type', kwargs={'pk': self.et.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 403)

        # Add permission to edit, user can now edit type
        self.user.user_permissions.add(*ensure_permissions(EquipmentType, ['change']))
        res = self.client.get(reverse('equipment-type', kwargs={'pk': self.et.id, 'action': 'edit'}))
        self.assertEqual(res.status_code, 200)

