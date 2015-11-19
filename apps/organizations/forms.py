__author__ = 'kako'

import itertools

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from ..resources.models import Employee, Equipment, Resource
from .models import Company, Team


class CompanyForm(OwnedEntityForm):

    class Meta:
        model = Company
        exclude = ('owner',)


class TeamForm(OwnedEntityForm):

    class Meta:
        model = Team
        exclude = ('owner',)

    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), required=False)
    equipment = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        # Restrict activities to workable only
        f = self.fields['activities']
        f.queryset = f.queryset.workable()

        # If it's a saved instance set initial values for related fields
        if self.instance.id:
            for k in ('employees', 'equipment'):
                f = self.fields[k]
                f.initial = f.queryset.filter(team=self.instance)

    def save(self, *args, **kwargs):
        res = super(TeamForm, self).save(*args, **kwargs)

        # Fetch resource ids from employees and equipment
        employees = self.cleaned_data['employees']
        equipment = self.cleaned_data['equipment']
        res_ids = list(itertools.chain(
            employees.values_list('resource_ptr_id', flat=True),
            equipment.values_list('resource_ptr_id', flat=True)
        ))

        # Remove unselected and add selected resources
        self.instance.resource_set.exclude(id__in=res_ids).update(team=None)
        Resource.objects.filter(id__in=res_ids).update(team=self.instance)

        # Return saved team instance
        return res


class CompanySearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Company code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Company name')


class TeamSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Team code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Team name')
    company__code__iexact = forms.CharField(max_length=32, required=False, label='Company')
