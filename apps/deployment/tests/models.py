
from django.test import TestCase

from ...accounts.factories import UserFactory
from ...common.test import mock
from ...organizations.factories import TeamFactory
from ...resources.factories import EmployeeFactory, EquipmentFactory
from ...work.factories import ActivityFactory, IndirectLabourFactory, DirectLabourFactory
from ..factories import TimeSheetFactory
from ..models import TimeSheet, TimeSheetAction, WorkLog, NotAuthorizedError


class TimeSheetTest(TestCase):

    def setUp(self):
        super(TimeSheetTest, self).setUp()

        # Main setup
        self.account = UserFactory.create().owner
        self.ts_settings = self.account.timesheet_settings
        self.dir = DirectLabourFactory.create()
        self.ind = IndirectLabourFactory.create()

        # Setup teams and create timesheet
        self.timekeeper = UserFactory.create(owner=self.account)
        self.supervisor1 = UserFactory.create(owner=self.account)
        self.supervisor2 = UserFactory.create(owner=self.account)
        self.team = TeamFactory.create(owner=self.account,
                                       timekeepers=[self.timekeeper],
                                       supervisors=[self.supervisor1, self.supervisor2])
        self.ts = TimeSheetFactory.create(owner=self.account,
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
        e1 = EmployeeFactory.create(team=self.team)
        e2 = EquipmentFactory.create()

        # Add a few activities, link team to last one
        a1 = ActivityFactory.create()
        a2 = ActivityFactory.create()
        a3 = ActivityFactory.create()
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
        self.account = UserFactory.create().owner
        self.ts_settings = self.account.timesheet_settings
        self.dir = DirectLabourFactory.create()
        self.ind = IndirectLabourFactory.create()

        # Setup users, teams and create timesheet
        self.user1 = UserFactory.create(owner=self.account)
        self.user2 = UserFactory.create()
        self.team = TeamFactory.create(owner=self.account)
        self.ts = TimeSheetFactory.create(owner=self.account, team=self.team)

    def test_filter_for_user(self):
        # Added this because something was failing, which was caused by the
        # worklog not setting its owner before saving, hehe
        WorkLog.objects.all().delete()
        self.assertNotEqual(self.user1.domain, self.user2.domain)
        self.assertNotEqual(None, self.user2.domain)

        # Create a few workflogs
        e = EmployeeFactory.create(team=self.team)
        a = ActivityFactory.create()
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

