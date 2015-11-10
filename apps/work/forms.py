__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from .models import Project, Activity


class ProjectForm(OwnedEntityForm):

    class Meta:
        model = Project
        exclude = ('owner',)


class ActivityForm(OwnedEntityForm):

    class Meta:
        model = Activity
        exclude = ('owner',)


class ProjectSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Project name')


class ActivitySearchForm(ModernForm):
    project__code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Activity name')
