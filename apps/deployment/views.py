
from ..common.views.base import StandardResourceView
from .models import TimeSheet
from .forms import TimeSheetForm, TimeSheetActionForm, WorkLogsForm, TimeSheetSearchForm


class TimeSheetView(StandardResourceView):
    model = TimeSheet
    list_template = 'timesheets.html'
    detail_template = 'timesheet.html'
    edit_template = 'timesheet-edit.html'
    main_form = TimeSheetForm
    sub_form = WorkLogsForm
    search_form = TimeSheetSearchForm


class TimeSheetActionView(StandardResourceView):
    model = TimeSheet
    list_template = 'timesheets.html'
    detail_template = 'timesheet.html'
    edit_template = 'timesheet-action-edit.html'
    main_form = TimeSheetActionForm
    permissions = {
        'add': ('issue', 'review',)
    }

