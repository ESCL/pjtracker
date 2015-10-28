
from ..common.views.base import StandardResourceView
from .models import TimeSheet


class TimeSheetView(StandardResourceView):
    model = TimeSheet
    list_template = 'timesheets.html'
    detail_template = 'timesheet.html'
