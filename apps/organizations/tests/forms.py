__author__ = 'kako'

from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import Group

from ...accounts.factories import UserFactory, User
from ...accounts.utils import ensure_permissions
from ...deployment.models import TimeSheet
from ...resources.factories import EmployeeFactory, EquipmentFactory
from ...work.models import LabourType
from ..factories import PositionFactory, CompanyFactory
from ..forms import TeamForm, PositionForm
from ..models import Team, Position, PositionLabourType


class TeamFormTest(TestCase):

    def setUp(self):
        super(TeamFormTest, self).setUp()

        # Create user and get account
        self.user = UserFactory.create(password='123')
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
        self.user.user_permissions.add(*ensure_permissions(Team, ['change activities']))

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
        self.user.user_permissions.add(*ensure_permissions(Team, ['change']))

        # Init form, now everything's editable
        self.user = User.objects.get(id=self.user.id)
        form = TeamForm(user=self.user)
        for k, field in form.fields.items():
            self.assertFalse('disabled' in field.widget.attrs)
            self.assertFalse('readonly' in field.widget.attrs)

    def test_limit_timesheet_assignment(self):
        # Make user a team manager to allow setting timekeepers and supervisors
        self.user.user_permissions.add(*ensure_permissions(Team, ['add', 'change']))

        # Render w/o timekeepers/supervisors, both fields are empty
        form = TeamForm(user=self.user)
        self.assertEqual(form.fields['timekeepers'].queryset.count(), 0)
        self.assertEqual(form.fields['supervisors'].queryset.count(), 0)

        # Add a timekeeper with direct permissions
        tk = UserFactory.create(owner=self.user.owner)
        tk.user_permissions.add(*ensure_permissions(TimeSheet, ['issue']))

        # Add a supervisor with indirect permissions (through group)
        g = Group.objects.create(name='supervisors')
        g.permissions.add(*ensure_permissions(TimeSheet, ['review']))
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

    def test_save(self):
        # Give first full permissions
        self.user.user_permissions.add(*ensure_permissions(Team, ['add', 'change']))
        self.user.user_permissions.add(*ensure_permissions(TimeSheet, ['issue', 'review']))

        # Create a team with 1 emp and 1 eqp
        emp = EmployeeFactory.create(owner=self.account)
        eqp = EquipmentFactory.create(owner=self.account)
        data = {'name': 'x', 'code': 'X',
                'company': CompanyFactory.create(owner=self.user.owner).id,
                'timekeepers': [self.user.id], 'supervisors': [self.user.id],
                'employees': [emp.id], 'equipment': [eqp.id]}
        form = TeamForm(data, user=self.user)
        self.assertTrue(form.is_valid())
        team = form.save()

        # Assert team was created with correct assignment
        self.assertEqual([e for e in team.employees], [emp])
        self.assertEqual([e for e in team.equipment], [eqp])

        # Remove equipment
        data['equipment'] = []
        form = TeamForm(data, user=self.user)
        self.assertTrue(form.is_valid())
        team = form.save()

        # Assert team was created with correct assignment
        self.assertEqual([e for e in team.employees], [emp])
        self.assertEqual([e for e in team.equipment], [])


class PositionFormTest(TestCase):

    def setUp(self):
        super(PositionFormTest, self).setUp()

        # Create user and account
        self.user = UserFactory.create(password='123')
        self.account = self.user.owner
        self.user.user_permissions.add(*ensure_permissions(Position, ['change']))

        # Add labour types
        self.ind = LabourType.objects.get(code='IN')
        self.dir = LabourType.objects.get(code='DI')

    def test_disabled_fields(self):
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

    def test_save(self):
        # Clear pos labour types to be sure
        PositionLabourType.objects.all().delete()
        Position.objects.all().delete()

        # New position with labour types
        data = {'name': 'Crane Operator', 'code': 'CRO',
                'pos_labour_types': [self.dir.id, self.ind.id]}
        form = PositionForm(data, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Assert pos was added, with two labour types for user
        self.assertEqual(Position.objects.count(), 1)
        self.assertEqual(PositionLabourType.objects.count(), 2)
        pos = Position.objects.get()
        self.assertEqual(pos.name, 'Crane Operator')
        self.assertEqual(set(pos.get_labour_types_for(self.user)), {self.dir, self.ind})

        # Update, removing indirect labour type
        plt_ids = {plt.id for plt in PositionLabourType.objects.all()}
        data['pos_labour_types'].pop()
        form = PositionForm(data, instance=pos, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Assert indirect was removed, direct remains (same id)
        self.assertEqual(Position.objects.count(), 1)
        self.assertEqual(PositionLabourType.objects.count(), 1)
        self.assertIn(PositionLabourType.objects.get().id, plt_ids)
        pos = Position.objects.get()
        self.assertEqual(list(pos.get_labour_types_for(self.user)), [self.dir])
