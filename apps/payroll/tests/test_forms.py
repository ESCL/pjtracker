__author__ = 'kako'

from django.test import TestCase

from ...accounts.factories import AccountFactory
from ..forms import CalendarDay, StandardHoursForm
from ..models import StandardHours


class StandardHoursFormTest(TestCase):

    def setUp(self):
        self.account = AccountFactory.create()

    def test_validate(self):
        # Init form, all fields empty
        form = StandardHoursForm(account=self.account)
        for k, f in form.fields.items():
            self.assertEqual(f.initial, 0)

        # Post with all fields empty, error
        form = StandardHoursForm({}, account=self.account)
        self.assertFalse(form.is_valid())

        # Post with some fields empty, error
        d = {'weekdays': 5}
        form = StandardHoursForm(d, account=self.account)
        self.assertFalse(form.is_valid())

        # Post correctly, OK
        d = {'weekdays': 5, 'saturdays': 0, 'sundays': 0, 'holidays': 0}
        form = StandardHoursForm(d, account=self.account)
        self.assertTrue(form.is_valid())

    def test_save(self):
        StandardHours.objects.all().delete()

        # Post and save with nothing, everything's created anyway
        d = {'weekdays': 0, 'saturdays': 0, 'sundays': 0, 'holidays': 0}
        form = StandardHoursForm(d, account=self.account)
        form.is_valid()
        form.save()
        self.assertEqual(StandardHours.objects.count(), 4)
        self.assertEqual(StandardHours.objects.filter(owner=self.account).count(), 4)
        res = {sh.day_type: sh.hours for sh in StandardHours.objects.all()}
        self.assertEqual(res, {CalendarDay.WEEKDAY: 0, CalendarDay.SATURDAY: 0,
                               CalendarDay.SUNDAY: 0, CalendarDay.PUBLIC_HOLIDAY: 0})

        # Post with single entry, everything's updated
        d = {'weekdays': 5, 'saturdays': 0, 'sundays': 0, 'holidays': 0}
        form = StandardHoursForm(d, account=self.account)
        form.is_valid()
        form.save()
        self.assertEqual(StandardHours.objects.count(), 4)
        res = {sh.day_type: sh.hours for sh in StandardHours.objects.all()}
        self.assertEqual(res, {CalendarDay.WEEKDAY: 5, CalendarDay.SATURDAY: 0,
                               CalendarDay.SUNDAY: 0, CalendarDay.PUBLIC_HOLIDAY: 0})

        # Post with all entries, one updated, three created
        d = {'weekdays': 8, 'saturdays': 4, 'sundays': 2, 'holidays': 1}
        form = StandardHoursForm(d, account=self.account)
        form.is_valid()
        form.save()
        self.assertEqual(StandardHours.objects.count(), 4)
        res = {sh.day_type: sh.hours for sh in StandardHours.objects.all()}
        self.assertEqual(res, {CalendarDay.WEEKDAY: 8, CalendarDay.SATURDAY: 4,
                               CalendarDay.SUNDAY: 2, CalendarDay.PUBLIC_HOLIDAY: 1})
