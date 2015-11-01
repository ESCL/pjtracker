__author__ = 'kako'

from django import forms

from .models import Project, Activity


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('owner',)


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        exclude = ('owner',)

