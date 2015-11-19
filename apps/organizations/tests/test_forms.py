__author__ = 'kako'

from django.test import TestCase
from unittest.mock import patch, MagicMock

from ...accounts.factories import UserFactory, User
from ...accounts.utils import create_permissions
from ..forms import TeamForm
from ..models import Team


class TeamFormTest(TestCase):

    def setUp(self):
        super(TeamFormTest, self).setUp()

        self.user = UserFactory.create()
        self.account = self.user.owner

    @patch('apps.work.query.ActivityQuerySet.workable', MagicMock(return_value=['lala']))
    def test_activities_queryset(self):
        # Init the form passing correct user
        form = TeamForm(user=self.user)

        # Make sure field qs was set to result of workable
        # Note: workable is already tested by activity model unit tests
        self.assertEqual(form.fields['activities'].queryset, ['lala'])

    def test_limited_permissions(self):
        # Add permissions to edit team activities
        self.user = User.objects.get(id=self.user.id)
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
