__author__ = 'kako'

from ..common.forms import OwnedEntityForm
from .models import Project, Activity


class ProjectForm(OwnedEntityForm):

    class Meta:
        model = Project
        exclude = ('owner',)


class ActivityForm(OwnedEntityForm):

    class Meta:
        model = Activity
        exclude = ('owner',)
