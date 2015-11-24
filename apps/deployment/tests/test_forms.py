
from datetime import date, timedelta

from django.test import TestCase

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...organizations.factories import TeamFactory
from ..forms import TimeSheetForm, TimeSheetActionForm
from ..models import TimeSheet


class TimeSheetFormTest(TestCase):

    def setUp(self):
        super(TimeSheetFormTest, self).setUp()

        # Setup user and team
        self.user = UserFactory.create()
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['create']))
        self.team = TeamFactory.create(owner=self.user.owner)

    def test_validate_unique(self):
        self.assertFalse(TimeSheet.objects.filter(team=self.team, date=date.today()).exists())

        # Try to create one for team1:today, ok
        form = TimeSheetForm({'team': self.team.id, 'date': date.today()}, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(TimeSheet.objects.filter(team=self.team, date=date.today()).exists())

        # Try to create the same, error
        form = TimeSheetForm({'team': self.team.id, 'date': date.today()}, user=self.user)
        self.assertFalse(form.is_valid())

        # Create for same team and tomorrow, OK
        tomorrow = date.today() + timedelta(days=1)
        form = TimeSheetForm({'team': self.team.id, 'date': tomorrow}, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(TimeSheet.objects.filter(team=self.team, date=tomorrow).exists())

    def test_ensure_owner(self):
        self.assertIsNotNone(self.team.owner)
        self.assertIsNotNone(self.user.owner)

        # Set user as global
        self.user.owner = None
        self.user.save()

        # Create a timesheet, instance has no account (same as user's)
        form = TimeSheetForm({'team': self.team.id, 'date': date.today()}, user=self.user)
        self.assertTrue(form.is_valid())

        # Save it, now account is the same as team's
        self.assertIsNone(form.instance.owner)
        form.save()
        self.assertEqual(form.instance.owner, self.team.owner)


class TimeSheetActionFormTest(TestCase):

    def setUp(self):
        super(TimeSheetActionFormTest, self).setUp()

        # Setup user and team and create timesheet
        self.user = UserFactory.create()
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['issue']))
        self.team = TeamFactory.create(owner=self.user.owner)
        self.ts = TimeSheet.objects.create(owner=self.user.owner, team=self.team, date=date.today())

    def test_clean(self):
        # Init form for render, make sure it does not break (issue #91)
        form = TimeSheetActionForm(instance=self.ts, user=self.user)
        self.assertEqual(form.user, self.user)

        # Now post issue, should be ok
        form = TimeSheetActionForm({'action': 'issue', 'feedback': ''}, instance=self.ts, user=self.user)
        self.assertTrue(form.is_valid())

        # Simulate issuance to allow testing rejection
        TimeSheet.objects.filter(pk=self.ts.id).update(status=TimeSheet.STATUS_ISSUED)
        self.ts = TimeSheet.objects.get(pk=self.ts.id)

        # Now post rejection w/o feedback, error
        form = TimeSheetActionForm({'action': 'reject', 'feedback': ''}, instance=self.ts, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertFalse('feedback' in form.cleaned_data)
        self.assertTrue('feedback' in form.errors)

        # Now post rejection with feedback, ok
        form = TimeSheetActionForm({'action': 'reject', 'feedback': 'bullshit, they were on stike!'},
                                   instance=self.ts, user=self.user)
        self.assertTrue(form.is_valid())
