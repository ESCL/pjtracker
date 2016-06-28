__author__ = 'kako'

from django import forms
from django.db.models import Q

from ..common.forms import OwnedEntityForm, OwnedEntitiesForm
from ..resources.models import Employee, Equipment
from ..work.models import LabourType
from .models import Company, Department, Team, Position


class CompanySearchForm(OwnedEntitiesForm):
    code__iexact = forms.CharField(max_length=8, required=False, label='Company code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Company name')


class DepartmentSearchForm(OwnedEntitiesForm):
    code__iexact = forms.CharField(max_length=8, required=False, label='Department code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Department name')


class PositionSearchForm(OwnedEntitiesForm):
    code__iexact = forms.CharField(max_length=8, required=False, label='Position code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Position name')


class TeamSearchForm(OwnedEntitiesForm):
    code__iexact = forms.CharField(max_length=8, required=False, label='Team code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Team name')
    company__code__iexact = forms.CharField(max_length=32, required=False, label='Company code')


class CompanyForm(OwnedEntityForm):

    class Meta:
        model = Company
        exclude = ('owner',)


class DepartmentForm(OwnedEntityForm):

    class Meta:
        model = Department
        exclude = ('owner',)


class PositionForm(OwnedEntityForm):

    class Meta:
        model = Position
        fields = ('name', 'code')

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

    # TODO: Handle "change employees" and "change equipment" permissions
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), required=False)
    equipment = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        # Restrict activities to workable only (field could be missing if form
        # is bound and user has no permissions to edit activities)
        f = self.fields.get('activities')
        if f:
            f.queryset = f.queryset.workable()

        # If it's a saved instance set initial values for related fields
        if self.instance.id:
            for k in 'employees', 'equipment':
                f = self.fields.get(k)
                if f:
                    f.initial = f.queryset.filter(team=self.instance)

        # Limit timesheet workflow assignment fields
        self._limit_timesheet_assignments()

    def _limit_timesheet_assignments(self):
        """
        Restrict timekeepers and supervisors querysets to users that are
        allowed to perform the actions required.
        """
        # Timekeepers: only those that can issue
        f = self.fields.get('timekeepers')
        if f:
            f.queryset = f.queryset.filter(
                Q(user_permissions__codename='issue_timesheet')|
                Q(groups__permissions__codename='issue_timesheet')
            )

        # Supervisors: only those that can review
        f = self.fields.get('supervisors')
        if f:
            f.queryset = f.queryset.filter(
                Q(user_permissions__codename='review_timesheet')|
                Q(groups__permissions__codename='review_timesheet')
            )

    def save(self, *args, **kwargs):
        team = super(TeamForm, self).save(*args, **kwargs)

        # Fetch resource ids from employees and equipment
        employees = self.cleaned_data['employees']
        equipment = self.cleaned_data['equipment']
        team.update_resources(employees=employees, equipment=equipment)

        # Return saved team instance
        return team
