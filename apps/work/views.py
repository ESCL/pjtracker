from django.shortcuts import render

from ..common.views.base import StandardResourceView
from .forms import ProjectForm, ActivityForm
from .models import Project, Activity


class ProjectView(StandardResourceView):
    model = Project
    list_template = 'projects.html'
    detail_template = 'project.html'
    edit_template = 'project-edit.html'
    main_form = ProjectForm


class ActivityView(StandardResourceView):
    model = Activity
    list_template = 'activities.html'
    detail_template = 'activity.html'
    edit_template = 'activity-edit.html'
    main_form = ActivityForm

    @classmethod
    def build_filters(cls, qs, **kwargs):
        filters = super(ActivityView, cls).build_filters(qs)
        filters['project'] = kwargs.get('project')
        return filters

    def show_list(self, request, status=200, pj_pk=None, **kwargs):
        if not pj_pk:
            raise ValueError("Project parameter missing.")

        pj = Project.objects.get(id=pj_pk)
        acts = self.filter_objects(request.user, request.GET, project=pj, **kwargs)
        context = {'activities': acts, 'project': pj}
        return render(request, self.list_template, context, status=status)
