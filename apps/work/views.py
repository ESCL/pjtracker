
from ..common.views.base import StandardResourceView
from .forms import ProjectForm, ActivityForm, ProjectSearchForm, ActivitySearchForm
from .models import Project, Activity


class ProjectView(StandardResourceView):
    model = Project
    list_template = 'projects.html'
    detail_template = 'project.html'
    edit_template = 'project-edit.html'
    main_form = ProjectForm
    search_form = ProjectSearchForm


class ActivityView(StandardResourceView):
    model = Activity
    list_template = 'activities.html'
    detail_template = 'activity.html'
    edit_template = 'activity-edit.html'
    main_form = ActivityForm
    search_form = ActivitySearchForm
