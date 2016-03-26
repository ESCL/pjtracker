__author__ = 'kako'

from django.test import TestCase

from ..factories import ActivityFactory, ProjectFactory
from ..models import Activity


class ActivityQuerySetTest(TestCase):

    def setUp(self):
        self.prj = ProjectFactory.create(code='HMS01')

    def test_get_by_wbs_path(self):
        # Create three hierarchical activities
        act1 = ActivityFactory.create(project=self.prj, code='ENG')
        act2 = ActivityFactory.create(parent=act1, code='TR1')
        act3 = ActivityFactory.create(parent=act2, code='DS56')

        # Get parent for act1, nothing
        parent = Activity.objects.get_by_wbs_path(['HMS01'] + act1.parent_wbs_path)
        self.assertIsNone(parent, None)

        # Get parent for act2: act1
        parent = Activity.objects.get_by_wbs_path(['HMS01'] + act2.parent_wbs_path)
        self.assertEqual(parent, act1)

        # Get parent for act3: act2
        parent = Activity.objects.get_by_wbs_path(['HMS01'] + act3.parent_wbs_path)
        self.assertEqual(parent, act2)

        # Get parent for fourth-level activity pointing to nothing: error
        self.assertRaises(Activity.DoesNotExist,
                          Activity.objects.get_by_wbs_path,
                          ['HMS01', 'ENG', 'WTF', 'DS56'])
