__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory, UserFakeFactory
from ...organizations.factories import TeamFakeFactory
from ...work.factories import ProjectFakeFactory
from ..models import Employee, Equipment


class CreteExampleResourcesTest(TestCase):

    def setUp(self):
        self.acc = AccountFakeFactory.create()
        self.u1 = UserFakeFactory.create(username='hr', owner=self.acc)
        self.u2 = UserFakeFactory.create(username='pcon', owner=self.acc)
        self.pj = ProjectFakeFactory.create(owner=self.acc)
        self.t1 = TeamFakeFactory.create(owner=self.acc)
        self.t2 = TeamFakeFactory.create(owner=self.acc)

    def test_create_example_resources(self):
        n_employees = Employee.objects.count()
        n_equipment = Equipment.objects.count()

        # Call command
        call_command('create_example_resources', self.acc.code)

        # Check number of companies and teams added
        self.assertEqual(Employee.objects.count(), n_employees + 4)
        self.assertEqual(Equipment.objects.count(), n_equipment + 1)

        # Check their data
        self.assertEqual(Employee.objects.filter(team=self.t1).count(), 2)
        self.assertEqual(Equipment.objects.filter(team=self.t1).count(), 0)
        self.assertEqual(Employee.objects.filter(team=self.t2).count(), 2)
        self.assertEqual(Equipment.objects.filter(team=self.t2).count(), 1)
