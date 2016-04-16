__author__ = 'kako'

from datetime import date

from django.test import TestCase

from ...common.exceptions import InvalidOperationError
from ...deployment.factories import TimeSheetFactory
from ...deployment.models import WorkLog, TimeSheet
from ...resources.factories import EmployeeFactory
from ...work.factories import ActivityFactory
from ...work.models import LabourType
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
        CalendarDay.objects.create(name='lol', date=date(2015, 12, 11), type=CalendarDay.PUBLIC_HOLIDAY)

        # Filter from the 7th to the 10th, all non-stored dates
        days = CalendarDay.objects.in_range(date(2015, 12, 7), date(2015, 12, 10))
        self.assertEqual(len(days), 4)
        for day, d_n in zip(days, (7, 8, 9, 10)):
            self.assertEqual(day.id, None)
            self.assertEqual(day.date, date(2015, 12, d_n))

        # Add the 11th, the first four weekdays are the same
        days = CalendarDay.objects.in_range(date(2015, 12, 7), date(2015, 12, 11))
        self.assertEqual(len(days), 5)
        for day, d_n in zip(days, (7, 8, 9, 10)):
            self.assertEqual(day.id, None)
            self.assertEqual(day.date, date(2015, 12, d_n))
            self.assertTrue(day.is_a(CalendarDay.WEEKDAY))

        # But friday is stored and a holiday
        day = days[4]
        self.assertEqual(type(day.id), int)
        self.assertEqual(day.date, date(2015, 12, 11))
        self.assertFalse(day.is_a(CalendarDay.WEEKDAY))
        self.assertTrue(day.is_a(CalendarDay.PUBLIC_HOLIDAY))


class WorkedHoursTest(TestCase):

    def setUp(self):
        # Create an activity and an employee
        self.mgt = LabourType.objects.get(code='MG')
        self.act = ActivityFactory.create(labour_types=[self.mgt])
        self.acc = self.act.owner
        self.emp = EmployeeFactory.create(owner=self.acc)
        self.team = self.emp.team

        # Create standard hour types (normal, OT 150%, OT 200%)
        self.n = NormalHoursFactory.create(owner=self.acc)
        self.ot150 = Overtime150HoursFactory.create(owner=self.acc)
        self.ot200 = Overtime200HoursFactory.create(owner=self.acc)

        # Set standard hours: Weekdays 9, saturdays 6
        StandardHours.objects.create(day_type=CalendarDay.WEEKDAY, hours=9, owner=self.acc)
        StandardHours.objects.create(day_type=CalendarDay.SATURDAY, hours=6, owner=self.acc)

        # Set normal ranges
        HourTypeRange.objects.create(day_type=CalendarDay.WEEKDAY, hour_type=self.n, limit=8)
        HourTypeRange.objects.create(day_type=CalendarDay.WEEKDAY, hour_type=self.ot150)
        HourTypeRange.objects.create(day_type=CalendarDay.SATURDAY, hour_type=self.ot150, limit=4)
        HourTypeRange.objects.create(day_type=CalendarDay.SATURDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(day_type=CalendarDay.SUNDAY, hour_type=self.ot200)
        HourTypeRange.objects.create(day_type=CalendarDay.PUBLIC_HOLIDAY, hour_type=self.ot200)

        # Make friday 25th a public holiday
        CalendarDay.objects.create(name='lol', date=date(2015, 12, 25), type=CalendarDay.PUBLIC_HOLIDAY)

        # Create a period forecasting the last week (28th to 3rd)
        self.period = Period.objects.create(start_date=date(2015, 12, 5),
                                            end_date=date(2016, 1, 3),
                                            forecast_start_date=date(2015, 12, 28))

        # Now add hours for the current week
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 21)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=8)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 22)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=10)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 23)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=4)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 24)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=12)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 25)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=4)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 26)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=6)

        # Approve all timesheets to get the results
        TimeSheet.objects.update(status=TimeSheet.STATUS_APPROVED)

    def test_create_error(self):
        # Try to create worked hours instance by queryset method, invalid op
        self.assertRaises(InvalidOperationError, WorkedHours.objects.create,
                          period=self.period, employee=self.emp, phase=WorkedHours.PHASE_ACTUAL,
                          hour_type=self.n, hours=20)

    def test_calculate_actual(self):
        # Calculate, should result in three WorkedHours instances
        res = list(WorkedHours.calculate_for_employee(self.period, WorkedHours.PHASE_ACTUAL, self.emp))
        self.assertEqual(len(res), 3)
        wh1, wh2, wh3 = res

        # Since friday is holiday normal hours = 8+8+4+8+0+0 = 28
        self.assertEqual(wh1.period, self.period)
        self.assertEqual(wh1.employee, self.emp)
        self.assertEqual(wh1.hour_type, self.n)
        self.assertEqual(wh1.hours, 28)

        # Overtime at 150 = 0+2+0+4+4+0 = 10
        self.assertEqual(wh2.period, self.period)
        self.assertEqual(wh2.employee, self.emp)
        self.assertEqual(wh2.hour_type, self.ot150)
        self.assertEqual(wh2.hours, 10)

        # Overtime at 200 = 0+0+0+0+0+6 = 6
        self.assertEqual(wh3.period, self.period)
        self.assertEqual(wh3.employee, self.emp)
        self.assertEqual(wh3.hour_type, self.ot200)
        self.assertEqual(wh3.hours, 6)

    def test_calculate_forecast(self):
        # Calculate, should result in three WorkedHours instances
        res = list(WorkedHours.calculate_for_employee(self.period, WorkedHours.PHASE_FORECAST, self.emp))
        self.assertEqual(len(res), 3)
        wh1, wh2, wh3 = res

        # Normal hours = 8+8+8+8+8+0 = 40
        self.assertEqual(wh1.period, self.period)
        self.assertEqual(wh1.employee, self.emp)
        self.assertEqual(wh1.hour_type, self.n)
        self.assertEqual(wh1.hours, 40)

        # Overtime at 150 = 1+1+1+1+1+4 = 9
        self.assertEqual(wh2.period, self.period)
        self.assertEqual(wh2.employee, self.emp)
        self.assertEqual(wh2.hour_type, self.ot150)
        self.assertEqual(wh2.hours, 9)

        # Overtime at 200 = 0+0+0+0+0+2 = 2
        self.assertEqual(wh3.period, self.period)
        self.assertEqual(wh3.employee, self.emp)
        self.assertEqual(wh3.hour_type, self.ot200)
        self.assertEqual(wh3.hours, 2)

    def test_calculate_adjustment(self):
        # Add a new period
        self.period2 = Period.objects.create(start_date=date(2016, 1, 4),
                                             end_date=date(2016, 2, 1),
                                             forecast_start_date=date(2016, 1, 25))

        # Calculate and save period 1 actual+forecast
        for wh in WorkedHours.calculate_for_employee(self.period, WorkedHours.PHASE_ACTUAL, self.emp):
            wh.save()
        for wh in WorkedHours.calculate_for_employee(self.period, WorkedHours.PHASE_FORECAST, self.emp):
            wh.save()

        # Now add period 1 retroactive hours (10 on weekdays, 7 on saturday)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 29)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=6)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2015, 12, 30)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=4)
        WorkLog.objects.create(timesheet=TimeSheetFactory.create(team=self.team, date=date(2016, 1, 2)),
                               resource=self.emp.resource_ptr, activity=self.act,
                               labour_type=self.mgt, hours=7)
        TimeSheet.objects.update(status=TimeSheet.STATUS_APPROVED)

        # Calculate and save period 1 retroactive WorkedHours
        for wh in WorkedHours.calculate_for_employee(self.period, WorkedHours.PHASE_RETROACTIVE, self.emp):
            wh.save()

        # Calculate adjustment for period 2
        res = list(WorkedHours.calculate_for_employee(self.period2, WorkedHours.PHASE_ADJUSTMENT, self.emp))
        self.assertEqual(len(res), 3)
        wh1, wh2, wh3 = res

        # Normal hours = 10 - 40 = -30
        self.assertEqual(wh1.period, self.period2)
        self.assertEqual(wh1.employee, self.emp)
        self.assertEqual(wh1.hour_type, self.n)
        self.assertEqual(wh1.hours, -30)

        # Overtime at 150 = 4 - 9 = -5
        self.assertEqual(wh2.period, self.period2)
        self.assertEqual(wh2.employee, self.emp)
        self.assertEqual(wh2.hour_type, self.ot150)
        self.assertEqual(wh2.hours, -5)

        # Overtime at 200 = 3 - 2 = 1
        self.assertEqual(wh3.period, self.period2)
        self.assertEqual(wh3.employee, self.emp)
        self.assertEqual(wh3.hour_type, self.ot200)
        self.assertEqual(wh3.hours, 1)
