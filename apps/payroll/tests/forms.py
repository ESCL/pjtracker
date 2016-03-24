__author__ = 'kako'

from django.test import TestCase

from ...accounts.factories import UserFactory
from ..forms import CalendarDay, HoursSettingsForm, ProcessPayrollForm
from ..models import HourTypeRange, StandardHours
from ..factories import NormalHoursFactory, Overtime150HoursFactory, Overtime200HoursFactory


class HoursSettingsFormTest(TestCase):

    def setUp(self):
        # Create account and a few hour types
        self.user = UserFactory.create()
        self.std = NormalHoursFactory.create(owner=self.user.owner)
        self.ot150 = Overtime150HoursFactory.create(owner=self.user.owner)
        self.ot200 = Overtime200HoursFactory.create(owner=self.user.owner)

    def test_validate(self):
        # Init form, all fields empty
        form = HoursSettingsForm(user=self.user)
        for k, f in form.fields.items():
            self.assertEqual(f.initial, 0)

        # Post with all fields empty, ok
        form = HoursSettingsForm({}, user=self.user)
        self.assertTrue(form.is_valid())

        # Post with average hours and no hour type ranges, invalid
        d = {'sh-weekdays': 8}
        form = HoursSettingsForm(d, user=self.user)
        self.assertFalse(form.is_valid())

        # Post with top range below min required (50% above avg), invalid
        d['htr-weekdays-STD'] = 9
        form = HoursSettingsForm(d, user=self.user)
        self.assertFalse(form.is_valid())

        # Post correctly, OK
        d.update({'htr-weekdays-STD': 8, 'htr-weekdays-OT150': 16})
        form = HoursSettingsForm(d, user=self.user)
        self.assertTrue(form.is_valid())

    def test_save(self):
        # Clear all hours config for account
        StandardHours.objects.filter(owner=self.user.owner).delete()
        HourTypeRange.objects.filter(owner=self.user.owner).delete()

        # Save empty form
        form = HoursSettingsForm({}, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Std hours are always saved (0 hours), ranges are not
        self.assertEqual(StandardHours.objects.filter(owner=self.user.owner).count(), 4)
        self.assertEqual(StandardHours.objects.filter(owner=self.user.owner, hours=0).count(), 4)
        self.assertEqual(HourTypeRange.objects.filter(owner=self.user.owner).count(), 0)
        sh_wd = StandardHours.objects.get(owner=self.user.owner, day_type=CalendarDay.WEEKDAY)

        # Post 8 std hours and two limits for weekday
        d = {'sh-weekdays': 8, 'htr-weekdays-STD': 8, 'htr-weekdays-OT150': 16}
        form = HoursSettingsForm(d, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Should have updated std hours on weekday and created two ranges
        self.assertEqual(StandardHours.objects.filter(owner=self.user.owner, hours=0).count(), 3)
        sh1 = StandardHours.objects.get(owner=self.user.owner, day_type=CalendarDay.WEEKDAY)
        self.assertEqual(sh1, sh_wd)
        self.assertEqual(sh1.hours, 8)
        self.assertEqual(HourTypeRange.objects.filter(owner=self.user.owner).count(), 2)
        htr1, htr2 = HourTypeRange.objects.filter(owner=self.user.owner).order_by('id').all()
        self.assertEqual(htr1.day_type, CalendarDay.WEEKDAY)
        self.assertEqual(htr1.hour_type, self.std)
        self.assertEqual(htr1.limit, 8)
        self.assertEqual(htr2.day_type, CalendarDay.WEEKDAY)
        self.assertEqual(htr2.hour_type, self.ot150)
        self.assertEqual(htr2.limit, 16)

        # Post modifs for weekday limits, add two for saturday
        d.update({'htr-weekdays-OT150': 12, 'htr-weekdays-OT200': 16,
                  'htr-saturdays-OT150': 4, 'htr-saturdays-OT200': 8})
        form = HoursSettingsForm(d, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Should have updated one (weekday+std) and added three
        self.assertEqual(HourTypeRange.objects.filter(owner=self.user.owner).count(), 5)
        htr1b, htr2b, htr3, htr4, htr5 = HourTypeRange.objects.filter(owner=self.user.owner).order_by('id').all()
        self.assertEqual(htr1b, htr1)
        self.assertEqual(htr2b, htr2)
        self.assertEqual(htr2b.day_type, CalendarDay.WEEKDAY)
        self.assertEqual(htr2b.hour_type, self.ot150)
        self.assertEqual(htr2b.limit, 12)
        self.assertEqual(htr3.day_type, CalendarDay.WEEKDAY)
        self.assertEqual(htr3.hour_type, self.ot200)
        self.assertEqual(htr3.limit, 16)
        self.assertEqual(htr4.day_type, CalendarDay.SATURDAY)
        self.assertEqual(htr4.hour_type, self.ot150)
        self.assertEqual(htr4.limit, 4)
        self.assertEqual(htr5.day_type, CalendarDay.SATURDAY)
        self.assertEqual(htr5.hour_type, self.ot200)
        self.assertEqual(htr5.limit, 8)


class ProcessPayrollFormTest(TestCase):

    def test_validate(self):
        # Form without data, invalid
        form = ProcessPayrollForm()
        self.assertFalse(form.is_valid())

        # Default confirm value, invalid
        form = ProcessPayrollForm({'confirm': 'no'})
        self.assertFalse(form.is_valid())

        # Confirm yes, valid
        form = ProcessPayrollForm({'confirm': 'yes'})
        self.assertTrue(form.is_valid())
