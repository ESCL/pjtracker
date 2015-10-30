
from django.test import TestCase

from ...accounts.factories import AccountFactory, UserFactory
from ...notifications.models import Notification
from ...organizations.factories import TeamFactory
from ..factories import TimeSheetFactory
from ..models import TimeSheet


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

