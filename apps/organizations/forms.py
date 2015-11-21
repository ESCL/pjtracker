__author__ = 'kako'

import itertools

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from ..resources.models import Employee, Equipment
from ..work.models import LabourType
from .models import Company, Team, Position


class CompanyForm(OwnedEntityForm):

    class Meta:
        model = Company
        exclude = ('owner',)


class PositionForm(OwnedEntityForm):

    class Meta:
        model = Position
        exclude = ('owner', 'labour_types',)

    pos_labour_types = forms.ModelMultipleChoiceField(queryset=LabourType.objects.all(),
                                                      required=False, label='Labour types')

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            f = self.fields['pos_labour_types']
            f.initial = self.instance.get_labour_types_for(self.user)

    def save(self, *args, **kwargs):
        pos = super(PositionForm, self).save(*args, **kwargs)

        # Update labour types, first remove and then add
        lts = self.cleaned_data['pos_labour_types']
        pos.update_labour_types(lts, self.user)

        # Return saved instance
        return pos


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
        team = super(TeamForm, self).save(*args, **kwargs)

        # Fetch resource ids from employees and equipment
        employees = self.cleaned_data['employees']
        equipment = self.cleaned_data['equipment']
        team.update_resources(employees=employees, equipment=equipment)

        # Return saved team instance
        return team


class CompanySearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Company code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Company name')


class PositionSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Position code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Position name')


class TeamSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Team code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Team name')
    company__code__iexact = forms.CharField(max_length=32, required=False, label='Company')
