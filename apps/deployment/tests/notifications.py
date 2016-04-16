__author__ = 'kako'

from django.test import TestCase

from apps.accounts.factories import UserFakeFactory
from apps.accounts.utils import ensure_permissions
from apps.notifications.models import Notification
from apps.deployment.factories import TimeSheetFakeFactory
from apps.deployment.models import TimeSheet
from apps.organizations.factories import TeamFakeFactory


class TimeSheetNotificationsTest(TestCase):

    def setUp(self):
        # Create one timekeeper and two reviewers
        self.tk = UserFakeFactory.create(user_permissions=ensure_permissions(TimeSheet, ['add', 'issue']))
        self.account = self.tk.owner
        self.r1 = UserFakeFactory.create(user_permissions=ensure_permissions(TimeSheet, ['review']), owner=self.account)
        self.r2 = UserFakeFactory.create(user_permissions=ensure_permissions(TimeSheet, ['review']), owner=self.account)

        # Create one team and and a timesheet
        self.team = TeamFakeFactory.create(owner=self.account, timekeepers=[self.tk], supervisors=[self.r1, self.r2])
        self.ts = TimeSheetFakeFactory.create(team=self.team, owner=self.account)

    def test_typical_workflow(self):
        Notification.objects.all().delete()

        # Issue timesheet
        self.ts.issue(self.tk)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)

        # Two new notifs for reviewers
        self.assertEqual(Notification.objects.enabled().count(), 2)
        self.assertEqual(Notification.objects.disabled().count(), 0)
        n1, n2 = Notification.objects.enabled()
        self.assertEqual(n1.recipient, self.r1)
        self.assertEqual(n1.event_target, self.ts)
        self.assertEqual(n1.event_type, 'issued')
        self.assertEqual(n2.recipient, self.r2)
        self.assertEqual(n2.event_target, self.ts)
        self.assertEqual(n2.event_type, 'issued')

        # One reviwer rejects
        self.ts.reject(self.r1)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_REJECTED)

        # Both notifs for reviewers dropped, 1 for timekeepes added
        self.assertEqual(Notification.objects.enabled().count(), 1)
        self.assertEqual(Notification.objects.disabled().count(), 2)
        n = Notification.objects.enabled()[0]
        self.assertEqual(n.recipient, self.tk)
        self.assertEqual(n.event_target, self.ts)
        self.assertEqual(n.event_type, 'rejected')

        # Issue again
        self.ts.issue(self.tk)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)

        # 2 added for reviwers, one dropped for timekeeper
        self.assertEqual(Notification.objects.enabled().count(), 2)
        self.assertEqual(Notification.objects.disabled().count(), 3)
        n1, n2 = Notification.objects.enabled()
        self.assertEqual(n1.recipient, self.r1)
        self.assertEqual(n1.event_target, self.ts)
        self.assertEqual(n1.event_type, 'issued')
        self.assertEqual(n2.recipient, self.r2)
        self.assertEqual(n2.event_target, self.ts)
        self.assertEqual(n2.event_type, 'issued')

        # One reviewer approves
        self.ts.approve(self.r1)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_ISSUED)

        # One dropped (for reviewer 1), remaining is n2 (from previous check)
        self.assertEqual(Notification.objects.enabled().count(), 1)
        self.assertEqual(Notification.objects.disabled().count(), 4)
        n = Notification.objects.enabled()[0]
        self.assertEqual(n, n2)

        # Another reviewer approves
        self.ts.approve(self.r2)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_APPROVED)

        # One more dropped, nothing left
        self.assertEqual(Notification.objects.enabled().count(), 0)
        self.assertEqual(Notification.objects.disabled().count(), 5)
