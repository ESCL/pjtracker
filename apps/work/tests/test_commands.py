__author__ = 'kako'

from django.core.management import call_command
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory
from ..models import Project, Activity


class CreateExampleProjectTest(TestCase):

    def setUp(self):
        # Create account
        self.acc = AccountFakeFactory.create()

    def tearDown(self):
        # Remove account and its objects
        self.acc.delete()

    def test_create_example_resources(self):
        # Call command
        call_command('create_example_project', self.acc.code)

        # Get project
        pj = Project.objects.get(owner=self.acc)

        # Check activities (22 overall, 8 workable)
        acts = Activity.objects.filter(project=pj)
        self.assertEqual(acts.count(), 22)
        self.assertEqual(acts.workable().count(), 8)
