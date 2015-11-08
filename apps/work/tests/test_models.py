from django.test import TestCase

from ...accounts.factories import UserFactory
from ..factories import ActivityFactory
from ..models import Activity


class ActivityTest(TestCase):

    def setUp(self):
        super(ActivityTest, self).setUp()

        # Create a user
        self.user = UserFactory.create()

    def test_filter_workable(self):
        # Create a global and an account activity
        g_act = ActivityFactory.create(owner=None)
        a_act = ActivityFactory.create(owner=self.user.owner)

        # Nothin workable
        self.assertEqual(Activity.objects.for_user(self.user).workable().count(), 0)

        # Allow indirect in global, is now selected filtered
        g_act.indirect_labour = True
        g_act.save()
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], g_act)

        # Allow account act direct, selected as well
        a_act.direct_labour = True
        a_act.save()
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(set(qs), {a_act, g_act})
