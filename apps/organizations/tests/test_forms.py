__author__ = 'kako'

from django.test import TestCase
from django.contrib.auth.models import Group

from ...common.test import mock
from ...accounts.factories import UserFactory, User
from ...accounts.utils import create_permissions
from ...deployment.models import TimeSheet
from ..factories import PositionFactory, CompanyFactory
from ..forms import TeamForm, PositionForm
from ..models import Team, Position


class TeamFormTest(TestCase):

    def setUp(self):
        super(TeamFormTest, self).setUp()

        self.user = UserFactory.create()
        self.account = self.user.owner

    @mock.patch('apps.work.query.ActivityQuerySet.workable',
                mock.MagicMock(return_value=['lala']))
    def test_activities_queryset(self):
        # Init the form passing correct user
        form = TeamForm(user=self.user)

        # Make sure field qs was set to result of workable
        # Note: workable is already tested by activity model unit tests
        self.assertEqual(form.fields['activities'].queryset, ['lala'])

    def test_limited_permissions(self):
        # Add permissions to edit team activities
        self.user.user_permissions.add(*create_permissions(Team, ['change activities']))

        # Init the form and calculate what fields should be editable
        form = TeamForm(user=self.user)
        # Note: Employees and equipment are also editable
        editable = ('activities', 'employees', 'equipment')
        for k in editable:
            field = form.fields[k]
            self.assertFalse('disabled' in field.widget.attrs)
            self.assertFalse('readonly' in field.widget.attrs)

        # Check that other fields are not editable
        readonly = set(form.fields.keys()).difference(editable)
        for k in readonly:
            field = form.fields[k]
            self.assertEqual(field.widget.attrs['disabled'], 'disabled')
            self.assertEqual(field.widget.attrs['readonly'], True)

        # Add full permissions to user
        self.user.user_permissions.add(*create_permissions(Team, ['change']))

        # Init form, now everything's editable
        self.user = User.objects.get(id=self.user.id)
        form = TeamForm(user=self.user)
        for k, field in form.fields.items():
            self.assertFalse('disabled' in field.widget.attrs)
            self.assertFalse('readonly' in field.widget.attrs)

    def test_limit_timesheet_assignment(self):
        # Make user a team manager to allow setting timekeepers and supervisors
        self.user.user_permissions.add(*create_permissions(Team, ['add', 'change']))

        # Render w/o timekeepers/supervisors, both fields are empty
        form = TeamForm(user=self.user)
        self.assertEqual(form.fields['timekeepers'].queryset.count(), 0)
        self.assertEqual(form.fields['supervisors'].queryset.count(), 0)

        # Add a timekeeper with direct permissions
        tk = UserFactory.create(owner=self.user.owner)
        tk.user_permissions.add(*create_permissions(TimeSheet, ['issue']))

        # Add a supervisor with indirect permissions (through group)
        g = Group.objects.create(name='supervisors')
        g.permissions.add(*create_permissions(TimeSheet, ['review']))
        s = UserFactory.create(owner=self.user.owner, groups=[g])

        # Render form again, they are both options
        form = TeamForm(user=self.user)
        self.assertEqual(set(form.fields['timekeepers'].queryset.all()), {tk})
        self.assertEqual(set(form.fields['supervisors'].queryset.all()), {s})

        # Post form with wrong timekeeper and supervisor, error
        cpy = CompanyFactory.create(owner=self.user.owner)
        data = {'name': 'x', 'company': cpy.id, 'code': 'X',
                'timekeepers': [s.id], 'supervisors': [tk.id]}
        form = TeamForm(data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertTrue('timekeepers' in form.errors)
        self.assertTrue('supervisors' in form.errors)

        # Post form with correct tk+sup, no errors there
        data.update({'timekeepers': [tk.id], 'supervisors': [s.id]})
        form = TeamForm(data, user=self.user)
        v = form.is_valid()
        self.assertTrue(v)


class PositionFormTest(TestCase):

    def setUp(self):
        super(PositionFormTest, self).setUp()

        self.user = UserFactory.create()
        self.account = self.user.owner

    def test_disabled_fields(self):
        # Add permissions to edit position
        self.user.user_permissions.add(*create_permissions(Position, ['change']))

        # Render empty form, everything's editable
        form = PositionForm(user=self.user)
        for f in form.fields.values():
            self.assertFalse('disabled' in f.widget.attrs)
            self.assertFalse('readonly' in f.widget.attrs)

        # Create account position and init form, everything's editable
        pos_a = PositionFactory.create(owner=self.account)
        form = PositionForm(user=self.user, instance=pos_a)
        for f in form.fields.values():
            self.assertFalse('disabled' in f.widget.attrs)
            self.assertFalse('readonly' in f.widget.attrs)

        # Create global position and init form
        pos_g = PositionFactory.create()
        form = PositionForm(user=self.user, instance=pos_g)

        # Labour types are editable
        self.assertFalse('disabled' in form.fields['pos_labour_types'].widget.attrs)
        self.assertFalse('readonly' in form.fields['pos_labour_types'].widget.attrs)

        # But nothing else is
        readonly = set(form.fields.keys()).difference({'pos_labour_types'})
        for k in readonly:
            f = form.fields[k]
            self.assertTrue('disabled' in f.widget.attrs)
            self.assertTrue('readonly' in f.widget.attrs)

