__author__ = 'kako'

from datetime import date

from django.test import TestCase

from ...deployment.factories import TimeSheetFactory
from ...deployment.models import WorkLog, TimeSheet
from ...resources.factories import EmployeeFactory
from ...work.factories import ActivityFactory, ManagementLabourFactory
from ..models import CalendarDay, HourTypeRange, Period, WorkedHours, StandardHours
from ..factories import NormalHoursFactory, Overtime150HoursFactory, Overtime200HoursFactory


class CalendarDayTest(TestCase):

    def test_type_assignment(self):
        # Init a monday, it's a weekday
        cd = CalendarDay(date=date(2015, 12, 7))
        self.assertEqual(cd.type, CalendarDay.WEEKDAY)

        # Init a friday, still a weekday
        cd = CalendarDay(date=date(2015, 12, 11))
        self.assertEqual(cd.type, CalendarDay.WEEKDAY)

        # Saturday
        cd = CalendarDay(date=date(2015, 12, 12))
        self.assertEqual(cd.type, CalendarDay.SATURDAY)

        # Sunday
        cd = CalendarDay(date=date(2015, 12, 13))
        self.assertEqual(cd.type, CalendarDay.SUNDAY)

        # Try to override, ignore
        cd = CalendarDay(date=date(2015, 12, 13), type=CalendarDay.WEEKDAY)
        self.assertEqual(cd.type, CalendarDay.SUNDAY)

        # Public holiday, always the same
        cd = CalendarDay(date=date(2015, 12, 7), type=CalendarDay.PUBLIC_HOLIDAY)
        self.assertEqual(cd.type, CalendarDay.PUBLIC_HOLIDAY)
        cd = CalendarDay(date=date(2015, 12, 13), type=CalendarDay.PUBLIC_HOLIDAY)
        self.assertEqual(cd.type, CalendarDay.PUBLIC_HOLIDAY)

    def test_is_a(self):
        # Is monday a weekday? Yes
        cd = CalendarDay(date=date(2015, 12, 7))
        self.assertTrue(cd.is_a(CalendarDay.WEEKDAY))

        # Is sunday a weekday? No
        cd = CalendarDay(date=date(2015, 12, 13))
        self.assertFalse(cd.is_a(CalendarDay.WEEKDAY))

        # Is saturday a saturday? Hehe
        cd = CalendarDay(date=date(2015, 12, 12))
        self.assertTrue(cd.is_a(CalendarDay.SATURDAY))

        # Public holiday? Only when we force it
        cd = CalendarDay(date=date(2015, 12, 12))
        self.assertFalse(cd.is_a(CalendarDay.PUBLIC_HOLIDAY))
        cd = CalendarDay(date=date(2015, 12, 12), type=CalendarDay.PUBLIC_HOLIDAY)
        self.assertTrue(cd.is_a(CalendarDay.PUBLIC_HOLIDAY))

    def test_filter_in_range(self):
        # Make friday a public holiday
        CalendarDay.objects.create(date=date(2015, 12, 11), type=CalendarDay.PUBLIC_HOLIDAY)

        # Filter from the 7th to the 10th, all non-stored dates
        days = CalendarDay.objects.in_range(date(2015, 12, 7), date(2015, 12, 10))
        self.assertEqual(len(days), 4)
        for day, d_n in zip(sorted(days.values()), (7, 8, 9, 10)):
            self.assertEqual(day.id, None)
            self.assertEqual(day.date, date(2015, 12, d_n))

        # Add the 11th, the first four are the same
        days = CalendarDay.objects.in_range(date(2015, 12, 7), date(2015, 12, 11))
        self.assertEqual(len(days), 5)
        for day, d_n in zip(sorted(days.values()), (7, 8, 9, 10)):
            self.assertEqual(day.id, None)
            self.assertEqual(day.date, date(2015, 12, d_n))

        # Last one has id (it's stored)
        day = sorted(days.values())[4]
        self.assertEqual(type(day.id), int)
        self.assertEqual(day.date, date(2015, 12, 11))


class WorkedHoursTest(TestCase):

    def setUp(self):
        # Create an activity and an employee
        self.lt = ManagementLabourFactory.create()
        self.act = ActivityFactory.create(labour_types=[self.lt])
        self.acc = self.act.owner
        self.emp = EmployeeFactory.create(owner=self.acc)
        self.team = self.emp.team

        # Create standard hour types (normal, OT 150%, OT 200%)
        self.n = NormalHoursFactory.create(owner=self.acc)
        self.ot150 = Overtime150HoursFactory.create(owner=self.acc)
        self.ot200 = Overtime200HoursFactory.create(owner=self.acc)

        # Weekdays, normal up to 8, 150 after that
        HourTypeRange.objects.create(day_type=CalendarDay.WEEKDAY, hour_type=self.n, limit=8)
        HourTypeRange.objects.create(day_type=CalendarDay.WEEKDAY, hour_type=self.ot150)

        # Saturday and sunday, 150 up to 4, 200 after that
        HourTypeRange.objects.create(day_type=CalendarDay.SATURDAY, hour_type=self.ot150, limit=4)
        HourTypeRange.objects.create(day_type=CalendarDay.SATURDAY, hour_type=self.ot200)

        # Sunday and public holidays all 200
        HourTypeRange.objects.create(day_type=CalendarDay.SUNDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(day_type=CalendarDay.PUBLIC_HOLIDAY, hour_type=self.ot200)

        # Make friday a public holiday
        CalendarDay.objects.create(date=date(2015, 12, 11), type=CalendarDay.PUBLIC_HOLIDAY)

    def test_calculate_actual(self):
        # Monday: 8 normal
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 7)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=8)

        # Tuesday: 8 normal + 2 at 150
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 8)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=10)

        # Wednesday: 4 normal
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 9)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=4)

        # Thursday: 8 normal + 4 at 150
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 10)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=12)

        # Holiday: 4 at 200
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 11)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=4)

        # Saturday: 4 at 150 + 2 at 200
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 12)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.lt, hours=6)

        # Approve all timesheets to get the results
        TimeSheet.objects.update(status=TimeSheet.STATUS_APPROVED)

        # Create one period
        period = Period.objects.create(start_date=date(2015, 12, 1),
                                       end_date=date(2015, 12, 31),
                                       forecast_start_date=date(2015, 12, 24))

        # Now calculate all hours for that employee
        res = WorkedHours.calculate(period, WorkedHours.PHASE_ACTUAL, self.emp)
        self.assertEqual(len(res), 3)
        wh1, wh2, wh3 = res

        # Normal hours, 36 in total
        self.assertEqual(wh1.period, period)
        self.assertEqual(wh1.employee, self.emp)
        self.assertEqual(wh1.hour_type, self.n)
        self.assertEqual(wh1.hours, 28)

        # Overtime at 150, 10 in total
        self.assertEqual(wh2.period, period)
        self.assertEqual(wh2.employee, self.emp)
        self.assertEqual(wh2.hour_type, self.ot150)
        self.assertEqual(wh2.hours, 10)

        # Overtime at 200, 6 in total
        self.assertEqual(wh3.period, period)
        self.assertEqual(wh3.employee, self.emp)
        self.assertEqual(wh3.hour_type, self.ot200)
        self.assertEqual(wh3.hours, 6)

    def test_calculate_forecast(self):
        # Weekdays 9, saturdays 6 (slave, dude!)
        StandardHours.objects.create(day_type=CalendarDay.WEEKDAY, hours=9, owner=self.acc)
        StandardHours.objects.create(day_type=CalendarDay.SATURDAY, hours=6, owner=self.acc)

        # Create one period
        period = Period.objects.create(start_date=date(2015, 12, 1),
                                       end_date=date(2015, 12, 31),
                                       forecast_start_date=date(2015, 12, 25))

        # Now calculate all hours for that employee
        res = WorkedHours.calculate(period, WorkedHours.PHASE_FORECAST, self.emp)
        self.assertEqual(len(res), 3)
        wh1, wh2, wh3 = res

        # Normal hours, 40 in total
        self.assertEqual(wh1.period, period)
        self.assertEqual(wh1.employee, self.emp)
        self.assertEqual(wh1.hour_type, self.n)
        self.assertEqual(wh1.hours, 40)

        # Overtime at 150, 9 in total
        self.assertEqual(wh2.period, period)
        self.assertEqual(wh2.employee, self.emp)
        self.assertEqual(wh2.hour_type, self.ot150)
        self.assertEqual(wh2.hours, 9)

        # Overtime at 200, 2 in total
        self.assertEqual(wh3.period, period)
        self.assertEqual(wh3.employee, self.emp)
        self.assertEqual(wh3.hour_type, self.ot200)
        self.assertEqual(wh3.hours, 2)
