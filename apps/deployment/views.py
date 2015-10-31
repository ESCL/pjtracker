
from django.views.generic import View

from ..common.views.base import StandardResourceView
from .models import TimeSheet
from .forms import EmployeeWorkLogsForm


class TimeSheetView(StandardResourceView):
    model = TimeSheet
    list_template = 'timesheets.html'
    detail_template = 'timesheet.html'
