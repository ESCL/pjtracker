__author__ = 'kako'

from django.test import TestCase

from ...accounts.utils import ensure_permissions
from ...accounts.factories import UserFakeFactory
from ..models import Activity, ActivityGroup
from ..factories import ProjectFakeFactory
from ..forms import ActivityForm


class ActivityFormTest(TestCase):

    def setUp(self):
        # Create one user with full permission to activities and a project
        self.user = UserFakeFactory.create(password='123')
        self.user.user_permissions.add(*ensure_permissions(Activity, ['add', 'change']))
        self.pj = ProjectFakeFactory.create(owner=self.user.owner)

        # Get two phase groups
        self.eng = ActivityGroup.objects.get(code='ENG')
        self.cst = ActivityGroup.objects.get(code='CST')

        # Get two discipline groups
        self.civ = ActivityGroup.objects.get(code='CIV')
        self.mec = ActivityGroup.objects.get(code='MEC')

    def test_groups(self):
        # Render form for new activity
        form = ActivityForm(user=self.user)

        # Check that "groups" field was replaced by two ("phase" and "discipline")
        self.assertFalse('groups' in form.fields)
        f_phase = form.fields['group_phase']
        f_disc = form.fields['group_discipline']

        # Make sure options are correct
        self.assertEqual(set(f_phase.queryset), set(ActivityGroup.objects.filter(type=self.cst.type)))
        self.assertEqual(set(f_disc.queryset), set(ActivityGroup.objects.filter(type=self.civ.type)))

        # Post and save
        data = {'project': self.pj.id, 'name': 'x', 'code': 'X',
                'group_phase': self.eng.id, 'group_discipline': self.civ.id}
        form = ActivityForm(data, user=self.user)
        form.is_valid()
        form.save()

        # Make sure the right groups were added
        act = Activity.objects.latest('id')
        self.assertEqual(set(act.groups.all()), {self.eng, self.civ})

        # Render form, make sure initial is selected
        form = ActivityForm(user=self.user, instance=act)
        f_phase = form.fields['group_phase']
        f_disc = form.fields['group_discipline']
        self.assertEqual(f_phase.initial, self.eng.id)
        self.assertEqual(f_disc.initial, self.civ.id)

        # Edit and select other groups, make sure they are updated
        data = {'project': self.pj.id, 'name': 'x', 'code': 'X',
                'group_phase': None, 'group_discipline': self.mec.id}
        form = ActivityForm(data, instance=act, user=self.user)
        form.is_valid()
        form.save()

        # Make sure the right groups were added
        act = Activity.objects.get(pk=act.id)
        self.assertEqual(set(act.groups.all()), {self.mec})
