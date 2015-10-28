from django.shortcuts import render

from ..common.views.base import StandardResourceView
from .models import Project


class ProjectView(StandardResourceView):
    model = Project
    list_template = 'projects.html'
    detail_template = 'project.html'
