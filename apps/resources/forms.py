__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from .models import Employee, Equipment


class EmployeeForm(OwnedEntityForm):

    class Meta:
        model = Employee
        exclude = ('owner', 'resource_type',)


class EquipmentForm(OwnedEntityForm):

    class Meta:
        model = Equipment
        exclude = ('owner', 'resource_type',)


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

