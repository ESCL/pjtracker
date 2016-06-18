from django.test import TestCase

from ...accounts.factories import UserFakeFactory, AccountFakeFactory
from ..factories import ProjectFakeFactory, ActivityFakeFactory
from ..models import Activity, LabourType


class ActivityTest(TestCase):

    def setUp(self):
        self.account = AccountFakeFactory.create()

    def test_init_set_parent(self):
        # Create a base activity
        prj = ProjectFakeFactory.create(owner=self.account, code='WOW')
        act1 = ActivityFakeFactory.create(code='CALI', project=prj, parent=None)
        self.assertEqual(act1.owner, self.account)

        # Now init a child w/o setting project. should set project to parent's
        act2 = Activity(parent=act1, code='LAX', name='Los Angeles Airport')
        self.assertEqual(act2.project, prj)
        self.assertEqual(act2.owner, self.account)

        # Now save it and init a child of that one with WBS code, should set parent and project
        act2.save()
        act3 = Activity(full_wbs_code='WOW.CALI.LAX.NODBT', name='No doubt, baby!')
        self.assertEqual(act3.parent, act2)
        self.assertEqual(act3.project, prj)
        self.assertEqual(act3.code, 'NODBT')
        self.assertEqual(act3.owner, self.account)

    def test_filter_workable(self):
        self.user = UserFakeFactory.create(password='123')

        # Create a global and an account activity
        g_act = ActivityFakeFactory.create(owner=None)
        a_act = ActivityFakeFactory.create(owner=self.user.owner)

        # Nothing workable
        self.assertEqual(Activity.objects.for_user(self.user).workable().count(), 0)

        # Allow indirect in global, is now selected filtered
        ind = LabourType.objects.get(code='IN')
        g_act.labour_types.add(ind)
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], g_act)

        # Allow account act direct, selected as well
        dir = LabourType.objects.get(code='DI')
        a_act.labour_types.add(dir)
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(set(qs), {a_act, g_act})
