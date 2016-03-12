from django.test import TestCase

from ...accounts.factories import UserFactory, AccountFactory
from ..factories import ProjectFactory, ActivityFactory, DirectLabourFactory, IndirectLabourFactory
from ..models import Activity, LabourType


class ActivityTest(TestCase):

    def setUp(self):
        self.account = AccountFactory.create()

    def test_init_set_parent(self):
        # Create a base activity
        prj = ProjectFactory.create(owner=self.account, code='WOW')
        act1 = ActivityFactory.create(code='CALI', project=prj, parent=None)
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
        self.user = UserFactory.create()

        # Create a global and an account activity
        g_act = ActivityFactory.create(owner=None)
        a_act = ActivityFactory.create(owner=self.user.owner)

        # Nothing workable
        self.assertEqual(LabourType.objects.count(), 0)
        self.assertEqual(Activity.objects.for_user(self.user).workable().count(), 0)

        # Allow indirect in global, is now selected filtered
        g_act.labour_types.add(IndirectLabourFactory.create())
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0], g_act)

        # Allow account act direct, selected as well
        a_act.labour_types.add(DirectLabourFactory.create())
        qs = Activity.objects.for_user(self.user).workable()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(set(qs), {a_act, g_act})
