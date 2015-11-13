
from datetime import date, timedelta

from django.test import TestCase

from ...accounts.factories import UserFactory
from ...accounts.utils import create_permissions
from ...organizations.factories import TeamFactory
from ..forms import TimeSheetForm
from ..models import TimeSheet


class TimeSheetFormTest(TestCase):

    def setUp(self):
        super(TimeSheetFormTest, self).setUp()

        # Setup teama and create timesheet
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
