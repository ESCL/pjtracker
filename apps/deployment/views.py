
from django.db.models import Sum

from ..common.views.base import StandardResourceView, ReadOnlyResourceView
from .models import TimeSheet, WorkLog
from .forms import TimeSheetForm, TimeSheetActionForm, WorkLogsForm, TimeSheetSearchForm, HoursSearchForm


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


class HoursView(ReadOnlyResourceView):
    model = WorkLog
    list_template = 'hours.html'
    search_form = HoursSearchForm

    @classmethod
    def get_list_context(cls, request, objs):
        ctx = super(HoursView, cls).get_list_context(request, objs)
        ctx['groups'] = request.GET.getlist('group_by') or ['project']
        return ctx

    def filter_objects(cls, user, qs, **kwargs):
        # We don't need to process the default filters
        objs = cls.model.objects.get_queryset()._filter_for_querystring(qs)
        objs = objs._group_for_querystring(qs)

        # Annotate and return
        return objs.annotate(total_hours=Sum('hours'))
