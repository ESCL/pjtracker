__author__ = 'kako'

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory, UserFakeFactory
from ...organizations.factories import TeamFakeFactory
from ..models import Employee, Equipment


class CreateExampleResourcesTest(TestCase):

    def setUp(self):
        # Create account
        self.acc = AccountFakeFactory.create()

        # Create teams and users required
        self.t1 = TeamFakeFactory.create(owner=self.acc, name='Engineering')
        self.t2 = TeamFakeFactory.create(owner=self.acc, name='Civil Works', company=self.t1.company)
        self.u1 = UserFakeFactory.create(owner=self.acc, groups=[Group.objects.get(name='Human Resources')])
        self.u2 = UserFakeFactory.create(owner=self.acc, groups=[Group.objects.get(name='Project Control')])

    def tearDown(self):
        # Remove account and its objects
        self.acc.delete()

    def test_create_example_resources(self):
        # Call command
        call_command('create_example_resources', self.acc.code)

        # Check number of companies and teams added
        employees = Employee.objects.filter(owner=self.acc)
        equipment = Equipment.objects.filter(owner=self.acc)
        self.assertEqual(employees.count(), 4)
        self.assertEqual(equipment.count(), 1)

        # Check their data
        self.assertEqual(employees.filter(team=self.t1).count(), 2)
        self.assertEqual(equipment.filter(team=self.t1).count(), 0)
        self.assertEqual(employees.filter(team=self.t2).count(), 2)
        self.assertEqual(equipment.filter(team=self.t2).count(), 1)
