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

    parent_id = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ActivityInlineForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            for key, field in self.fields.items():
                field.initial = getattr(self.instance, key)

            if not self.is_bound and self.instance.parent:
                self.fields['parent_id'].widget.attrs['value'] = self.instance.parent_id


class ActivityInlineFormSet(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ActivityInlineFormSet, self).__init__(*args, **kwargs)
        self._new_start = 1000000
        self._new_objs = {}

    def _get_parent(self, parent_id):
        if not parent_id:
            return None
        return self._objects[parent_id]

    def save_new(self, form, commit=True):
        form_n = int(form.prefix.split('-')[-1])
        self._new_start = min(form_n, self._new_start)
        return super(ActivityInlineFormSet, self).save_new(form, commit=commit)

    def save_parents(self):
        for form in self.forms[self._new_start:]:
            obj_id = form.prefix.split('-')[-1]
            self._new_objs[obj_id] = form.instance
            parent_id = form.cleaned_data['parent_id']
            if not parent_id:
                continue

            try:
                parent_id = int(parent_id)
            except ValueError:
                parent_id = parent_id.split('-')[1]
                form.instance.parent = self._new_objs[parent_id]
                form.instance.save()
            else:
                form.instance.parent_id = parent_id
                form.instance.save()


class ProjectSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Project name')


class ActivitySearchForm(ModernForm):
    project__code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Activity name')
