from unittest.mock import MagicMock, patch

from django.test import TestCase

from ...notifications.models import Notification
from ..factories import TimeSheetFactory
from ..models import TimeSheet


class TimeSheetTest(TestCase):

    def setUp(self):
        super(TimeSheetTest, self).setUp()
        self.ts = TimeSheetFactory.create()

    @patch('apps.notifications.models.Notification.objects.create', MagicMock())
    def test_timesheet_issued(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(self.ts.status, TimeSheet.STATUS_PREPARING)

        # Issue, should update status and call notify
        self.ts.issue(self.ts.issuer)

        # Reject, should update status and call notify
        self.ts.reject()


