from datetime import date
from unittest import mock

from django.test import TestCase

from ...accounts.factories import UserFakeFactory
from ...organizations.factories import TeamFakeFactory
from ...resources.factories import EmployeeFakeFactory, EquipmentFakeFactory
from ...work.factories import ActivityFakeFactory
from ...work.models import LabourType
from ..factories import TimeSheetFakeFactory, ResourceProjectAssignmentFakeFactory
from ..models import TimeSheet, TimeSheetAction, WorkLog, NotAuthorizedError, ResourceProjectAssignment


class TimeSheetTest(TestCase):

    def setUp(self):
        super(TimeSheetTest, self).setUp()

        # Main setup
        self.account = UserFakeFactory.create(password='123').owner
        self.ts_settings = self.account.timesheet_settings
        self.dir = LabourType.objects.get(code='DI')
        self.ind = LabourType.objects.get(code='IN')

        # Setup teams and create timesheet
        self.timekeeper = UserFakeFactory.create(owner=self.account, password='123')
        self.supervisor1 = UserFakeFactory.create(owner=self.account, password='123')
        self.supervisor2 = UserFakeFactory.create(owner=self.account, password='123')
        self.team = TeamFakeFactory.create(owner=self.account,
                                       timekeepers=[self.timekeeper],
                                       supervisors=[self.supervisor1, self.supervisor2])
        self.ts = TimeSheetFakeFactory.create(owner=self.account,
                                          team=self.team)

    @mock.patch('apps.deployment.models.TimeSheet.signal', mock.MagicMock())
    def test_reviews(self):
        # Issue and check reviews, nothing
        self.ts.issue(self.timekeeper)
        self.assertEqual(self.ts.active_reviews, [])
        self.assertEqual(self.ts.pending_reviews, {self.supervisor1, self.supervisor2})

        # Add an approval, still nothing because prop is cached
        self.ts.approve(self.supervisor1)
        self.assertEqual(self.ts.active_reviews, [])
        self.assertEqual(self.ts.pending_reviews, {self.supervisor1, self.supervisor2})

        # Fetch from db, now we get the review
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(len(self.ts.active_reviews), 1)
        rev = self.ts.active_reviews[0]
        self.assertEqual(rev.actor, self.supervisor1)
        self.assertEqual(rev.action, rev.APPROVED)
        self.assertEqual(self.ts.pending_reviews, {self.supervisor2})

        # Add a rejection, 2 reviews
        self.ts.reject(self.supervisor2)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(len(self.ts.active_reviews), 2)
        rev = self.ts.active_reviews[1]
        self.assertEqual(rev.actor, self.supervisor2)
        self.assertEqual(rev.action, rev.REJECTED)
        self.assertEqual(self.ts.pending_reviews, set())

        # Issue again, now no reviews
        self.ts.issue(self.timekeeper)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.active_reviews, [])
        self.assertEqual(self.ts.pending_reviews, {self.supervisor1, self.supervisor2})

    @mock.patch('apps.deployment.models.TimeSheet.signal', mock.MagicMock())
    def test_issue(self):
        self.assertEqual(self.ts.status, TimeSheet.STATUS_PREPARING)

        # Try to issue with supervisor, error
        self.assertRaises(NotAuthorizedError, self.ts.issue, self.supervisor1)

        # Issue the timesheet
        self.ts.issue(self.timekeeper)

        # Check that status and action were updated
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)
        action = TimeSheetAction.objects.latest('timestamp')
        self.assertEqual(action.actor, self.timekeeper)
        self.assertEqual(action.action, TimeSheetAction.ISSUED)

    @mock.patch('apps.deployment.models.TimeSheet.signal', mock.MagicMock())
    def test_reject(self):
        # Issue the timesheet
        self.ts.issue(self.timekeeper)

        # Try to reject with worker, error
        self.assertRaises(NotAuthorizedError, self.ts.reject, self.timekeeper)

        # Reject the timesheet
        self.ts.reject(self.supervisor1)

        # Make sure status and action are updated
        self.assertEqual(self.ts.status, TimeSheet.STATUS_REJECTED)
        action = TimeSheetAction.objects.latest('timestamp')
        self.assertEqual(action.actor, self.supervisor1)
        self.assertEqual(action.action, TimeSheetAction.REJECTED)

    @mock.patch('apps.deployment.models.TimeSheet.signal', mock.MagicMock())
    def test_approve(self):
        # Issue the timesheet
        self.ts.issue(self.timekeeper)

        # Try to approve with worker, error
        self.assertRaises(NotAuthorizedError, self.ts.approve, self.timekeeper)

        # Approve the timesheet
        self.ts.approve(self.supervisor1)

        # Status was not updated yet, since default approval policy is ALL
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)
        action = TimeSheetAction.objects.latest('timestamp')
        self.assertEqual(action.actor, self.supervisor1)
        self.assertEqual(action.action, TimeSheetAction.APPROVED)

        # Approve again, should know update status
        self.ts.approve(self.supervisor2)

        # Now it was updated, but still not notifs created
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_APPROVED)
        action = TimeSheetAction.objects.latest('timestamp')
        self.assertEqual(action.actor, self.supervisor2)
        self.assertEqual(action.action, TimeSheetAction.APPROVED)

    def test_work_logs_properties(self):
        # All properties are empty first
        self.assertEqual(self.ts.work_logs_data, {})
        self.assertEqual(self.ts.resources, {})

        # Add two resources, one belonging to the team
        e1 = EmployeeFakeFactory.create(team=self.team)
        e2 = EquipmentFakeFactory.create()

        # Add a few activities, link team to last one
        a1 = ActivityFakeFactory.create()
        a2 = ActivityFakeFactory.create()
        a3 = ActivityFakeFactory.create()
        self.team.activities.add(a1)

        # Fetch again, employees and acts are updated
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.resources, {e1.resource_ptr.id: e1.resource_ptr})
        self.assertEqual(self.ts.activities, {a1.id: a1})

        # Add a few logs with employees and activities not belonging to team
        log1 = WorkLog.objects.create(timesheet=self.ts,
                                      resource=e2.resource_ptr,
                                      activity=a2,
                                      hours=3,
                                      labour_type=self.ind)
        log2 = WorkLog.objects.create(timesheet=self.ts,
                                      resource=e2.resource_ptr,
                                      activity=a3,
                                      hours=5,
                                      labour_type=self.dir)

        # Fetch again, everything updated (and what belongs to team is first)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.work_logs_data, {e2.resource_ptr: {a2: log1, a3: log2}})
        self.assertEqual(self.ts.resources, {e1.resource_ptr.id: e1.resource_ptr,
                                             e2.resource_ptr.id: e2.resource_ptr})
        self.assertEqual(self.ts.activities, {a1.id: a1, a2.id: a2, a3.id: a3})


class WorkLogTest(TestCase):

    def setUp(self):
        super(WorkLogTest, self).setUp()

        # Main setup
        self.account = UserFakeFactory.create(password='123').owner
        self.ts_settings = self.account.timesheet_settings
        self.dir = LabourType.objects.get(code='DI')
        self.ind = LabourType.objects.get(code='IN')

        # Setup users, teams and create timesheet
        self.user1 = UserFakeFactory.create(owner=self.account, password='123')
        self.user2 = UserFakeFactory.create(password='123')
        self.team = TeamFakeFactory.create(owner=self.account)
        self.ts = TimeSheetFakeFactory.create(owner=self.account, team=self.team)

    def test_filter_for_user(self):
        # Added this because something was failing, which was caused by the
        # worklog not setting its owner before saving, hehe
        WorkLog.objects.all().delete()
        self.assertNotEqual(self.user1.domain, self.user2.domain)
        self.assertNotEqual(None, self.user2.domain)

        # Create a few workflogs
        e = EmployeeFakeFactory.create(team=self.team)
        a = ActivityFakeFactory.create()
        WorkLog.objects.create(timesheet=self.ts, resource=e.resource_ptr,
                               activity=a, hours=3, labour_type=self.ind)
        WorkLog.objects.create(timesheet=self.ts, resource=e.resource_ptr,
                               activity=a, hours=5, labour_type=self.dir)

        # User1 (in same account) can see the hours
        res = WorkLog.objects.for_user(self.user1)
        self.assertEqual(res.count(), 2)

        # User2 (another account) CANNOT see the hours
        res = WorkLog.objects.for_user(self.user2)
        self.assertEqual(res.count(), 0)

    def test_group_by(self):
        # Create a few work logs
        e1 = EmployeeFakeFactory.create(team=self.team)
        e2 = EmployeeFakeFactory.create(team=self.team)
        a1 = ActivityFakeFactory.create()
        a2 = ActivityFakeFactory.create()
        WorkLog.objects.create(timesheet=self.ts, resource=e1.resource_ptr,
                               activity=a1, hours=2, labour_type=self.ind)
        WorkLog.objects.create(timesheet=self.ts, resource=e1.resource_ptr,
                               activity=a2, hours=5, labour_type=self.ind)
        WorkLog.objects.create(timesheet=self.ts, resource=e2.resource_ptr,
                               activity=a1, hours=3, labour_type=self.dir)
        WorkLog.objects.create(timesheet=self.ts, resource=e2.resource_ptr,
                               activity=a2, hours=4, labour_type=self.ind)
        self.assertEqual(WorkLog.objects.filter(timesheet=self.ts).count(), 4)

        # Group by date, a single work log with only timesheet attr
        wlogs = WorkLog.objects.filter(timesheet=self.ts).group_for_querystring(['date']).distinct()
        self.assertEqual(wlogs.count(), 1)
        wl1 = wlogs.get()
        self.assertEqual(wl1.timesheet.id, self.ts.id)
        self.assertFalse(hasattr(wl1, 'resource'))
        self.assertFalse(hasattr(wl1, 'activity'))
        self.assertFalse(hasattr(wl1, 'labour_type'))

        # Group by employee only, two logs with only employee set
        wlogs = WorkLog.objects.filter(timesheet=self.ts).group_for_querystring(['resource']).distinct()
        self.assertEqual(wlogs.count(), 2)
        wl1, wl2 = wlogs.all()
        self.assertEqual(wl1.resource, e1.resource_ptr)
        self.assertFalse(hasattr(wl1, 'activity'))
        self.assertFalse(hasattr(wl1, 'labour_type'))
        self.assertEqual(wl2.resource, e2.resource_ptr)
        self.assertFalse(hasattr(wl2, 'activity'))
        self.assertFalse(hasattr(wl2, 'labour_type'))

        # Group by activity+labour type, three logs
        wlogs = WorkLog.objects.filter(timesheet=self.ts).group_for_querystring(['activity', 'labour_type']).distinct()
        self.assertEqual(wlogs.count(), 3)
        wl1, wl2, wl3 = wlogs.all()
        self.assertFalse(hasattr(wl1, 'resource'))
        self.assertEqual(wl1.activity, a1)
        self.assertEqual(wl1.labour_type, self.ind)
        self.assertFalse(hasattr(wl2, 'resource'))
        self.assertEqual(wl2.activity, a2)
        self.assertEqual(wl2.labour_type, self.ind)
        self.assertFalse(hasattr(wl3, 'resource'))
        self.assertEqual(wl3.activity, a1)
        self.assertEqual(wl3.labour_type, self.dir)


class ResourceProjectAssignmentTest(TestCase):

    def setUp(self):
        self.res = EmployeeFakeFactory.create().resource_ptr
        ResourceProjectAssignment.objects.all().delete()

    def test_in_dates(self):
        start_date = date(2016, 1, 1)
        end_date = date(2016, 12, 31)

        # Not collisions, empty qs
        self.assertFalse(ResourceProjectAssignment.objects.in_dates(start_date, end_date).exists())

        # Add two non-collisions
        # 1. Start and end before
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2015, 2, 20), end_date=date(2015, 12, 31)
        )
        # 2. Start later, never end
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2017, 1, 1)
        )

        # Still empty
        self.assertEqual(ResourceProjectAssignment.objects.in_dates(start_date, end_date).count(), 0)

        # Add 4 collisions
        # 1. Start before, end in the middle
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2015, 2, 20), end_date=date(2016, 4, 20)
        )
        # 2. Start in the middle, end after
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2016, 2, 20), end_date=date(2017, 2, 19)
        )
        # 3. Start before, end later
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2015, 2, 20), end_date=date(2017, 2, 19)
        )
        # 4. Start in the middle, never end
        ResourceProjectAssignmentFakeFactory.create(
            resource=self.res,
            start_date=date(2016, 6, 20)
        )

        # Now we get all collisions
        self.assertEqual(ResourceProjectAssignment.objects.in_dates(start_date, end_date).count(), 4)
