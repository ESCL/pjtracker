__author__ = 'kako'

from django import forms
from django.template.defaultfilters import slugify

from ..common.forms import OwnedEntityForm, ModernForm
from .models import Project, Activity, ActivityGroup, ActivityGroupType, LabourType


# Search forms for list views

class ProjectSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Project name')


class ActivitySearchForm(ModernForm):
    project__code__iexact = forms.CharField(max_length=16, required=False, label='Project code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Activity name')


class ActivityGroupSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Group code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Group name')
    type = forms.ModelChoiceField(queryset=ActivityGroupType.objects.all(), label='Type')


class ActivityGroupTypeSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Type code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Type name')


class LabourTypeSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Labour type code')
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Labour type name')


# Edit forms for edit views

class ProjectForm(OwnedEntityForm):

    class Meta:
        model = Project
        exclude = ('owner',)


class ActivityForm(OwnedEntityForm):

    class Meta:
        model = Activity
        exclude = ('owner', 'groups',)

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)

        # Fetch the group types for this account
        self.group_types = ActivityGroupType.objects.for_user(self.user)

        # Now add one field per type
        for gt in self.group_types:
            self.fields['group_{}'.format(slugify(gt.name))] = forms.ModelChoiceField(
                queryset=ActivityGroup.objects.filter(type=gt),
                required=False, label=gt.name,
            )

        # Now add the initial values if instance exists
        if self.instance.id:
            groups = {g.type_id: g.id for f in self.instance.groups.all()}
            for gt in self.group_types:
                g = groups.get(gt.id)
                if g:
                    self.fields['group_{}'.format(slugify(gt.name))].initial = g

    def save(self, commit=True):
        # Get final list of groups
        groups = []
        for gt in self.group_types:
            val = self.cleaned_data.pop('group_{}'.format(slugify(gt.name)))
            if val:
                groups.append(val)

        # Save, update groups and return
        # Note: the second save only updates the m2m, it's not really redundant
        obj = super(ActivityForm, self).save()
        obj.groups = groups
        return obj.save()


class ActivityGroupForm(OwnedEntityForm):

    class Meta:
        model = ActivityGroup
        exclude = ('owner',)


class ActivityGroupTypeForm(OwnedEntityForm):

    class Meta:
        model = ActivityGroupType
        exclude = ('owner',)


class LabourTypeForm(OwnedEntityForm):

    class Meta:
        model = LabourType
        exclude = ('owner',)


# Forms for experimental Project WBS edit view

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
    """
    Inline form set that allows saving new nested activities correctly,
    even when their parents are new.
    """
    def __init__(self, *args, **kwargs):
        super(ActivityInlineFormSet, self).__init__(*args, **kwargs)
        self._new_objs = {}

    def save_new(self, form, commit=True):
        """
        Save new instance and store its id keyed with its form prefix number
        to allowed fetching it later.
        """
        obj = super(ActivityInlineFormSet, self).save_new(form, commit=commit)

        # Store new instance id
        self._new_objs[form.prefix] = obj.id
        return obj

    def _get_parent_id(self, pk):
        """
        Get the parent id as integer from the field value, which could be
        a real id (for existing object) or a form prefix (for new ones).
        """
        if not pk.isdigit():
            pk = self._new_objs[pk]
        return int(pk)

    def save_parents(self):
        """
        Save all parents for changed forms.
        """
        # TODO: Find out why has_changed is always true, fix it
        for form in self.forms:
            if form.has_changed():
                parent_id = form.cleaned_data['parent_id']
                if parent_id:
                    form.instance.parent_id = self._get_parent_id(parent_id)
                    form.instance.save()

    def save(self, commit=True):
        res = super(ActivityInlineFormSet, self).save(commit=commit)
        self.save_parents()
        return res

