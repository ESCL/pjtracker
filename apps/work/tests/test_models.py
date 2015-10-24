from django.test import TestCase

from ..factories import ActivityFactory


class FactoryTests(TestCase):

    def test_complex_factories(self):
        # Create an activity, make sure groups were added
        activity = ActivityFactory.create()
        self.assertEqual(activity.groups.count(), 2)
