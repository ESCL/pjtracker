__author__ = 'kako'

from django.test import TestCase
from unittest.mock import patch, MagicMock

from ...accounts.factories import UserFactory, User
from ...accounts.utils import create_permissions
from ..forms import TeamForm
from ..models import Team


class TeamFormTest(TestCase):

    def setUp(self):
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
        self.user.user_permissions.add(*create_permissions(Team, ['change activities']))

        # In form only activities field is editable
        self.user = User.objects.get(id=self.user.id)
        form = TeamForm(user=self.user)
        field = form.fields['activities']
        self.assertFalse('disabled' in field.widget.attrs)
        self.assertFalse('readonly' in field.widget.attrs)
        readonly = set(form.fields.keys())
        readonly.remove('activities')
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
