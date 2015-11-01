from django.shortcuts import render

from ..common.views.base import StandardResourceView
from .models import Company, Team


class CompanyView(StandardResourceView):
    model = Company
    list_template = 'companies.html'
    detail_template = 'team.html'
    edit_template = 'team-edit.html'


class TeamView(StandardResourceView):
    model = Team
    list_template = 'teams.html'
    detail_template = 'team.html'
    edit_template = 'team-edit.html'

