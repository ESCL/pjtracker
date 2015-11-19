__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from .models import Employee, Equipment


class EmployeeForm(OwnedEntityForm):

    class Meta:
        model = Employee
        # Team assignment is managed in team form
        exclude = ('owner', 'resource_type', 'team',)


class EquipmentForm(OwnedEntityForm):

    class Meta:
        model = Equipment
        # Team assignment is managed in team form
        exclude = ('owner', 'resource_type', 'team',)


class EmployeeSearchForm(ModernForm):
    identifier = forms.CharField(max_length=16, required=False, label='Employee identifier')
    name = forms.CharField(max_length=32, required=False, label='Employee name')

    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)


class EquipmentSearchForm(ModernForm):
    identifier = forms.CharField(max_length=16, required=False, label='Equipment identifier')
    type = forms.CharField(max_length=32, required=False, label='Equipment type')

    def __init__(self, *args, **kwargs):
        super(EquipmentSearchForm, self).__init__(*args, **kwargs)

