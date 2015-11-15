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


class ActivityInlineForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ('code', 'name', 'labour_types', 'groups', 'parent_id',)
        extra = 0

    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ActivityInlineForm, self).__init__(*args, **kwargs)

        if self.instance:
            for key, field in self.fields.items():
                field.initial = getattr(self.instance, key)

            if not self.is_bound and self.instance.parent:
                self.fields['parent_id'].widget.attrs['value'] = self.instance.parent_id


class ProjectSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Project name')


class ActivitySearchForm(ModernForm):
    project__code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Activity name')
