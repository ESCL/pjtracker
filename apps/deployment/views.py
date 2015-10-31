
from django.shortcuts import redirect, render
from django.views.generic import View

from ..common.views.base import StandardResourceView
from ..organizations.models import Team
from .models import TimeSheet
from .forms import TimeSheetForm, TeamActivityForm, WorkLogsForm


class TimeSheetView(StandardResourceView):
    model = TimeSheet
    list_template = 'timesheets.html'
    detail_template = 'timesheet.html'
    edit_template = 'timesheet-edit.html'
    edit_form = TimeSheetForm
    redirect_view_name = 'timesheets'


class WorkLogsView(View):
    template = 'worklogs-edit.html'
    form = WorkLogsForm
    redirect_view_name = 'timesheets'

    def get_timesheet(self, pk):
        return TimeSheet.objects.get(id=pk)

    def get(self, request, timesheet_pk=None):
        timesheet = self.get_timesheet(timesheet_pk)
        form = self.form(timesheet)
        context = {'timesheet': timesheet, 'form': form}
        return render(request, self.template, context)

    def post(self, request, timesheet_pk=None):
        timesheet = self.get_timesheet(timesheet_pk)
        form = self.form(timesheet)

        if form.is_valid():
            form.process_logs()
            return redirect(self.redirect_view_name)

        else:
            context = {'timesheet': timesheet, 'form': form}
            return render(request, self.template, context)


class TeamActivityView(View):
    template = 'team-activities.html'

    def get(self, request, team_id, date):
        team = Team.objects.get(pk=team_id)
        form = TeamActivityForm(request.user, team)
        context = {'team': team, 'date': date, 'form': form}
        return render(request, self.template, context)

    def post(self, request, team_id, date):
        team = Team.objects.get(pk=team_id)
        form = TeamActivityForm(request.user, team, request.POST)
        context = {'team': team, 'date': date, 'form': form}
