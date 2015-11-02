
from ..common.views.base import StandardResourceView
from .forms import CompanyForm, TeamForm
from .models import Company, Team


class CompanyView(StandardResourceView):
    model = Company
    list_template = 'companies.html'
    detail_template = 'company.html'
    edit_template = 'company-edit.html'
    main_form = CompanyForm


class TeamView(StandardResourceView):
    model = Team
    list_template = 'teams.html'
    detail_template = 'team.html'
    edit_template = 'team-edit.html'
    main_form = TeamForm
