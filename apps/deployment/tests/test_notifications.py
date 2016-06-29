from django.test import TestCase
from django.contrib.auth.models import Group

from ...accounts.factories import UserFakeFactory
from ...accounts.utils import ensure_permissions
from ...notifications.models import Notification
from ...organizations.factories import TeamFakeFactory
from ...resources.factories import EquipmentFakeFactory
from ...work.factories import ProjectFakeFactory
from ..factories import TimeSheetFakeFactory, ResourceProjectAssignmentFakeFactory
from ..models import TimeSheet


class ResourceProjectAssignmentNotificationsTest(TestCase):

    def setUp(self):
        # Create one hr officer and two project managers
        self.hr = UserFakeFactory.create(groups=[Group.objects.get(name='Human Resources')])
        self.account = self.hr.owner
        self.pm1 = UserFakeFactory.create(groups=[Group.objects.get(name='Project Management')], owner=self.account)
        self.pm2 = UserFakeFactory.create(groups=[Group.objects.get(name='Project Management')], owner=self.account)

        # Create project with both managers and assignment
        self.pj = ProjectFakeFactory.create(owner=self.account, managers=[self.pm1, self.pm2])
        self.eqp = EquipmentFakeFactory.create(owner=self.account)
        self.rpa = ResourceProjectAssignmentFakeFactory.create(owner=self.account, project=self.pj, resource=self.eqp)

        # Clear all notifs
        Notification.objects.all().delete()

    def test_typical_workflow(self):
        # Issue assignment
        self.rpa.issue(self.hr)

        # Two new notifs for managers
        self.assertEqual(Notification.objects.enabled().count(), 2)
        self.assertEqual(Notification.objects.disabled().count(), 0)
        n1, n2 = Notification.objects.enabled()
        self.assertEqual(n1.recipient, self.pm1)
        self.assertEqual(n1.event_target, self.rpa)
        self.assertEqual(n1.event_type, 'issued')
        self.assertEqual(n2.recipient, self.pm2)
        self.assertEqual(n2.event_target, self.rpa)
        self.assertEqual(n2.event_type, 'issued')

        # One manager rejects
        self.rpa.refresh_from_db()
        self.rpa.reject(self.pm1)

        # Both notifs for managers dropped, 1 for hr added
        self.assertEqual(Notification.objects.enabled().count(), 1)
        self.assertEqual(Notification.objects.disabled().count(), 2)
        n = Notification.objects.enabled()[0]
        self.assertEqual(n.recipient, self.hr)
        self.assertEqual(n.event_target, self.rpa)
        self.assertEqual(n.event_type, 'rejected')

        # hr issues it again
        self.rpa.refresh_from_db()
        self.rpa.issue(self.hr)

        # Two notifs added for managers, one dropped for hr
        self.assertEqual(Notification.objects.enabled().count(), 2)
        self.assertEqual(Notification.objects.disabled().count(), 3)
        n1, n2 = Notification.objects.enabled()
        self.assertEqual(n1.recipient, self.pm1)
        self.assertEqual(n1.event_target, self.rpa)
        self.assertEqual(n1.event_type, 'issued')
        self.assertEqual(n2.recipient, self.pm2)
        self.assertEqual(n2.event_target, self.rpa)
        self.assertEqual(n2.event_type, 'issued')

        # Second manager approves
        self.rpa.refresh_from_db()
        self.rpa.approve(self.pm2)

        # All notifs dropped
        self.assertEqual(Notification.objects.enabled().count(), 0)
        self.assertEqual(Notification.objects.disabled().count(), 5)


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

        # Clear all notifs just in case
        Notification.objects.all().delete()

    def test_typical_workflow(self):
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

        # One reviewer rejects
        self.ts.reject(self.r1)
        self.ts = TimeSheet.objects.get(id=self.ts.id)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_REJECTED)

        # Both notifs for reviewers dropped, 1 for timekeeper added
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

        # 2 added for reviewers, one dropped for timekeeper
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
