from django.shortcuts import render

from ..common.views.base import StandardResourceView
from .models import Project


class ProjectView(StandardResourceView):
    model = Project
