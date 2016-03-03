
import itertools
from datetime import date, timedelta

from django.test import TestCase

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...common.test import mock
from ...organizations.factories import TeamFactory
from ...resources.factories import EmployeeFactory
from ...work.factories import ActivityFactory, IndirectLabourFactory, DirectLabourFactory
from ..forms import TimeSheetForm, TimeSheetActionForm, TimeSheetSettingsForm, WorkLogsForm
from ..factories import TimeSheetFactory
from ..models import TimeSheet, WorkLog


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

    def test_clean(self):
        # Add one direct employee and one w/o labour type
        emp1 = EmployeeFactory.create(team=self.team)
        emp1.position.add_labour_type(self.dir)
        emp2 = EmployeeFactory.create(team=self.team)

        # Add three activities (one direct, one indirect, one w/oi labour type)
        act1 = ActivityFactory.create(labour_types=[self.dir])
        act2 = ActivityFactory.create(labour_types=[self.ind])
        act3 = ActivityFactory.create()
        self.team.activities.add(act1, act2, act3)

        # Attempt failed charge of hours
        # emp1+act1 : OK, emp1+act2: incompatible emp2+act3: activity cannot charge
        # emp2+act1: res cannot charge
        data = {str(emp1.resource_ptr_id): self.dir.id,
                '{}.{}'.format(emp1.resource_ptr_id, act1.id): 3,
                '{}.{}'.format(emp1.resource_ptr_id, act2.id): 3,
                '{}.{}'.format(emp1.resource_ptr_id, act3.id): 2,
                '{}.{}'.format(emp2.resource_ptr_id, act1.id): 8}
        form = WorkLogsForm(data, instance=self.ts, user=self.user)
        self.assertFalse(form.is_valid())
        nfe1, nfe2, nfe3 = form.non_field_errors()

        # field 2: value missing
        self.assertEqual(form.errors[str(emp2.resource_ptr_id)],
                         ['This field is required.'])

        # field 1.2: act1 cannot charge indirect
        self.assertIn(str(act2), nfe1)
        self.assertIn('does not allow charging hours', nfe1)
        self.assertIn(str(self.dir), nfe1)

        # field 1.3: act cannot charge
        self.assertIn(str(act3), nfe2)
        self.assertIn('does not allow charging hours', nfe2)

        # field 2.1: res cannot charge
        self.assertIn(str(emp2), nfe3)
        self.assertIn('cannot charge hours', nfe3)

    def test_save(self):
        # Clear all worklogs, just in case
        WorkLog.objects.all().delete()
        self.assertEqual(WorkLog.objects.count(), 0)

        # Create one emp and two acts, all compatible
        emp = EmployeeFactory.create(team=self.team)
        emp.position.add_labour_type(self.dir)
        act1 = ActivityFactory.create(labour_types=[self.dir])
        act2 = ActivityFactory.create(labour_types=[self.dir])
        self.team.activities.add(act1, act2)

        # Post 4 hours each
        data = {str(emp.resource_ptr_id): self.dir.id,
                '{}.{}'.format(emp.resource_ptr_id, act1.id): 4,
                '{}.{}'.format(emp.resource_ptr_id, act2.id): 4}
        form = WorkLogsForm(data, instance=self.ts, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Check work logs created
        self.assertEqual(WorkLog.objects.count(), 2)
        wl1, wl2 = WorkLog.objects.all()
        self.assertEqual(wl1.resource.instance, emp)
        self.assertEqual(wl1.activity, act1)
        self.assertEqual(wl1.hours, 4)
        self.assertEqual(wl2.resource.instance, emp)
        self.assertEqual(wl2.activity, act2)
        self.assertEqual(wl2.hours, 4)

        # Post 8 hours for first one
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        data.update({
            '{}.{}'.format(emp.resource_ptr_id, act1.id): 8.0,
            '{}.{}'.format(emp.resource_ptr_id, act2.id): 0.0
        })
        form = WorkLogsForm(data, instance=self.ts, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Check worklogs: one updated, one removed
        self.assertEqual(WorkLog.objects.count(), 1)
        wl = WorkLog.objects.get()
        self.assertEqual(wl.resource.instance, emp)
        self.assertEqual(wl.activity, act1)
        self.assertEqual(wl.hours, 8)
