__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory, UserFakeFactory
from ..models import Company, Team


class CreteExampleCompanyTest(TestCase):

    def setUp(self):
        self.acc = AccountFakeFactory.create()
        self.u1 = UserFakeFactory.create(username='supervisor')
        self.u2 = UserFakeFactory.create(username='timekeeper')

    def test_create_example_account(self):
        n_companies = Company.objects.count()
        n_teams = Team.objects.count()

        # Call command
        call_command('create_example_company')

        # Check number of companies and teams added
        self.assertEqual(Company.objects.count(), n_companies + 1)
        self.assertEqual(Team.objects.count(), n_teams + 2)

        # Check their data
        cpy = Company.objects.last()
        self.assertEqual(Team.objects.filter(company=cpy).count(), 2)
        t1, t2 = Team.objects.all()[n_teams:]
        self.assertEqual(t1.name, 'Engineering')
        self.assertEqual(t2.name, 'Civil Works')
