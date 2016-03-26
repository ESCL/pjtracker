
from ..common.views.base import StandardResourceView
from .forms import CompanyForm, TeamForm, CompanySearchForm, TeamSearchForm, PositionForm, PositionSearchForm
from .models import Company, Team, Position


class CompanyView(StandardResourceView):
    model = Company
    list_template = 'companies.html'
    detail_template = 'company.html'
    edit_template = 'company-edit.html'
    main_form = CompanyForm
    search_form = CompanySearchForm
    permissions = {
        'add': ('organizations.add_company',),
        'edit': ('organizations.change_company',),
    }


class PositionView(StandardResourceView):
    model = Position
    list_template = 'positions.html'
    detail_template = 'position.html'
    edit_template = 'position-edit.html'
    main_form = PositionForm
    search_form = PositionSearchForm
    permissions = {
        'add': ('organizations.add_position',),
        'edit': ('organizations.change_position',
                 'organizations.change_position_labour_types'),
    }


class TeamView(StandardResourceView):
    model = Team
    list_template = 'teams.html'
    detail_template = 'team.html'
    edit_template = 'team-edit.html'
    main_form = TeamForm
    search_form = TeamSearchForm
    permissions = {
        'add': ('organizations.add_team',),
        'edit': ('organizations.change_team',
                 'organizations.change_team_activities',)
    }
