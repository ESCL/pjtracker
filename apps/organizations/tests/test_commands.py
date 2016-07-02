__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory, UserFakeFactory
from ..models import Company, Team


class CreateExampleCompanyTest(TestCase):

    def setUp(self):
        # Create account
        self.acc = AccountFakeFactory.create()

    def tearDown(self):
        # Delete account (and all objects)
        self.acc.delete()

    def test_create_example_company(self):
        # Call command
        call_command('create_example_company', self.acc.code)

        # Check number of companies and teams added
        self.assertEqual(Company.objects.filter(owner=self.acc).count(), 1)
        self.assertEqual(Team.objects.filter(owner=self.acc).count(), 2)

        # Check their data
        cpy = Company.objects.get(owner=self.acc)
        t1, t2 = Team.objects.filter(owner=self.acc)
        self.assertEqual(t1.name, 'Engineering')
        self.assertEqual(t1.company, cpy)
        self.assertEqual(t1.name, 'Engineering')
        self.assertEqual(t2.company, cpy)
