
from django.test import TestCase

from ...accounts.factories import AccountFactory, UserFactory
from ...notifications.models import Notification
from ...organizations.factories import TeamFactory
from ...resources.factories import EmployeeFactory, EquipmentFactory
from ...work.factories import ActivityFactory
from ..factories import TimeSheetFactory
from ..models import TimeSheet, WorkLog, LabourType


class TimeSheetTest(TestCase):

    def setUp(self):
        super(TimeSheetTest, self).setUp()
        self.account = AccountFactory.create()
        self.worker = UserFactory.create(profile__account=self.account)
        self.supervisor = UserFactory.create(profile__account=self.account)
        self.team = TeamFactory.create(supervisor=self.supervisor)
        self.ts = TimeSheetFactory.create(issuer=self.worker, team=self.team)

    def test_timesheet_issued(self):
        self.assertEqual(self.ts.status, TimeSheet.STATUS_PREPARING)

        # Issue the timesheet
        self.ts.issue(self.worker)

        # Make sure status and worker were set correctly
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)
        self.assertEqual(self.ts.issuer, self.worker)
        self.assertEqual(self.ts.reviewer, None)

        # Make sure the notification for supervisor was created correctly
        notif = Notification.objects.latest('timestamp')
        self.assertEqual(notif.recipient, self.supervisor)
        self.assertEqual(notif.event_target, self.ts)
        self.assertEqual(notif.event_type, 'issued')
        self.assertEqual(notif.title, 'TimeSheet Issued')

    def test_timesheet_rejected(self):
        # Issue the timesheet
        self.ts.issue(self.worker)
        self.assertEqual(self.ts.reviewer, None)

        # Try to reject with worker, error
        self.assertRaises(TypeError, self.ts.reject, self.worker)

        # Reject the timesheet
        self.ts.reject(self.supervisor)

        # Make sure status and reviewer were set correctly
        self.assertEqual(self.ts.status, TimeSheet.STATUS_REJECTED)
        self.assertEqual(self.ts.reviewer, self.supervisor)

        # Make sure the notification for issuer was created correctly
        notif = Notification.objects.latest('timestamp')
        self.assertEqual(notif.recipient, self.worker)
        self.assertEqual(notif.event_target, self.ts)
        self.assertEqual(notif.event_type, 'rejected')
        self.assertEqual(notif.title, 'TimeSheet Rejected')

    def test_timesheet_approved(self):
        # Issue the timesheet
        self.ts.issue(self.worker)
        self.assertEqual(self.ts.reviewer, None)

        # Try to approve with worker, error
        self.assertRaises(TypeError, self.ts.approve, self.worker)

        # Reject the timesheet
        self.ts.approve(self.supervisor)

        # Make sure status and reviewer were set correctly
        self.assertEqual(self.ts.status, TimeSheet.STATUS_APPROVED)
        self.assertEqual(self.ts.reviewer, self.supervisor)

        # Make sure the notification for issuer was created correctly
        notif = Notification.objects.latest('timestamp')
        self.assertEqual(notif.recipient, self.worker)
        self.assertEqual(notif.event_target, self.ts)
        self.assertEqual(notif.event_type, 'approved')
        self.assertEqual(notif.title, 'TimeSheet Approved')

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
                                      labour_type=LabourType.INDIRECT)
        log2 = WorkLog.objects.create(timesheet=self.ts,
                                      resource=e2.resource_ptr,
                                      activity=a3,
                                      hours=5,
                                      labour_type=LabourType.INDIRECT)

        # Fetch again, everything updated (and what belongs to team is first)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.work_logs_data, {e2.resource_ptr: {a2: log1, a3: log2}})
        self.assertEqual(self.ts.resources, {e1.resource_ptr.id: e1.resource_ptr,
                                             e2.resource_ptr.id: e2.resource_ptr})
        self.assertEqual(self.ts.activities, {a1.id: a1, a2.id: a2, a3.id: a3})
