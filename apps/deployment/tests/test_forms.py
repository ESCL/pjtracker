
from datetime import date, timedelta
import itertools

from django.test import TestCase

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...common.test import mock
from ...organizations.factories import TeamFactory
from ...resources.factories import EmployeeFactory
from ...work.factories import ActivityFactory, IndirectLabourFactory, DirectLabourFactory
from ..forms import TimeSheetForm, TimeSheetActionForm, TimeSheetSettingsForm, WorkLogsForm
from ..factories import TimeSheetFactory
from ..models import TimeSheet


class TimeSheetFormTest(TestCase):

    def setUp(self):
        super(TimeSheetFormTest, self).setUp()

        # Setup user and team
        self.user = UserFactory.create()
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['create']))
        self.team = TeamFactory.create(owner=self.user.owner)

    def test_init(self):
        # Init without instance, team and no comments fields
        form = TimeSheetForm(user=self.user)
        self.assertTrue('team' in form.fields)
        self.assertFalse('comments' in form.fields)

        # Init with unsaved instance, team and no comments fields
        ts = TimeSheetFactory.build(owner=self.user.owner, team=self.team, date=date.today())
        form = TimeSheetForm(instance=ts, user=self.user)
        self.assertTrue('team' in form.fields)
        self.assertFalse('comments' in form.fields)

        # Init with saved instance, team and no comments fields
        ts.save()
        form = TimeSheetForm(instance=ts, user=self.user)
        self.assertFalse('team' in form.fields)
        self.assertTrue('comments' in form.fields)

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
        self.assertIsNone(form.instance.owner)

        # Save it, now account is the same as team's
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

    @mock.patch('apps.deployment.models.TimeSheet.issue', mock.MagicMock())
    @mock.patch('apps.deployment.models.TimeSheet.approve', mock.MagicMock())
    @mock.patch('apps.deployment.models.TimeSheet.reject', mock.MagicMock())
    def test_save(self):
        # Post an issue, should call issue
        form = TimeSheetActionForm({'action': 'issue', 'feedback': ''}, instance=self.ts, user=self.user)
        form.is_valid()
        form.save()
        TimeSheet.issue.assert_called_once_with(self.user)
        self.assertFalse(TimeSheet.approve.called)
        self.assertFalse(TimeSheet.reject.called)
        TimeSheet.issue.reset_mock()

        # Post an approval, should call approve
        self.ts.status = TimeSheet.STATUS_ISSUED
        form = TimeSheetActionForm({'action': 'approve', 'feedback': ''}, instance=self.ts, user=self.user)
        form.is_valid()
        form.save()
        self.assertFalse(TimeSheet.issue.called)
        TimeSheet.approve.assert_called_once_with(self.user)
        self.assertFalse(TimeSheet.reject.called)
        TimeSheet.approve.reset_mock()

        # Post an rejection, should call reject
        form = TimeSheetActionForm({'action': 'reject', 'feedback': 'that is so wrong'}, instance=self.ts, user=self.user)
        form.is_valid()
        form.save()
        self.assertFalse(TimeSheet.issue.called)
        self.assertFalse(TimeSheet.approve.called)
        TimeSheet.reject.assert_called_once_with(self.user)


class TimeSheetSettingsFormTest(TestCase):

    def test_validate(self):
        # Both approval and rejection ALL, invalid
        data = {'approval_policy': TimeSheet.REVIEW_POLICY_ALL,
                'rejection_policy': TimeSheet.REVIEW_POLICY_ALL}
        f = TimeSheetSettingsForm(data)
        self.assertFalse(f.is_valid())

        # Make rejection majority (see https://github.com/ESCL/pjtracker/issues/1)
        data['rejection_policy'] = TimeSheet.REVIEW_POLICY_MAJORITY
        f = TimeSheetSettingsForm(data)
        self.assertFalse(f.is_valid())

        # Make rejection majority (bug?)
        data['rejection_policy'] = TimeSheet.REVIEW_POLICY_FIRST
        f = TimeSheetSettingsForm(data)
        self.assertTrue(f.is_valid())


class WorkLogsFormTest(TestCase):

    def setUp(self):
        # Setup user and team and create timesheet
        self.user = UserFactory.create()
        self.user.user_permissions.add(*create_permissions(TimeSheet, ['issue']))
        self.team = TeamFactory.create(owner=self.user.owner)
        self.ts = TimeSheet.objects.create(owner=self.user.owner, team=self.team, date=date.today())

        # Add labour types
        self.dir = DirectLabourFactory.create()
        self.ind = IndirectLabourFactory.create()

    def test_init_alerts(self):
        # Team has no resources and no acts, should have alerts
        form = WorkLogsForm(instance=self.ts, user=self.user)
        self.assertEqual(form.alerts, ['This team has no resources assigned.',
                                       'This team has no activities assigned.'])

        # Assign activities and employees w/o matching labour types
        employee = EmployeeFactory.create(team=self.team)
        employee.position.add_labour_type(self.dir)
        activity = ActivityFactory.create(labour_types=[self.ind])
        self.team.activities.add(activity)

        # Now alert should say they don't match
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        form = WorkLogsForm(instance=self.ts, user=self.user)
        self.assertEqual(form.alerts, ['Labour types for activities and resources '
                                       'assigned to this team do not match.'])

    def test_disabled_fields(self):
        # Add two employees (one direct, one indirect)
        emp1 = EmployeeFactory.create(team=self.team)
        emp1.position.add_labour_type(self.dir)
        emp2 = EmployeeFactory.create(team=self.team)
        emp2.position.add_labour_type(self.ind)

        # Add two activities (one direct, one direct+indirect)
        act1 = ActivityFactory.create(labour_types=[self.dir])
        act2 = ActivityFactory.create(labour_types=[self.dir, self.ind])
        self.team.activities.add(act1, act2)

        # Should have no alerts
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        form = WorkLogsForm(instance=self.ts, user=self.user)
        self.assertEqual(form.alerts, [])

        # Check fields names
        field_names = {'{}.{}'.format(e.id, a.id) for e, a in
                       itertools.product((emp1, emp2), (act1, act2))}
        field_names.update({str(emp1.id), str(emp2.id)})
        self.assertEqual(set(form.fields.keys()), field_names)

        # Check disabled fields, only 2.1 (emp2, act1)
        disabled_fields = {fn for fn in field_names if
                           form.fields[fn].widget.attrs.get('disabled') == 'disabled'}
        self.assertEqual(disabled_fields, {'{}.{}'.format(emp2.id, act1.id)})

