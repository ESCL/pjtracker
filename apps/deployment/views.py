
from django.shortcuts import render
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
    main_form = TimeSheetForm
    sub_form = WorkLogsForm


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
