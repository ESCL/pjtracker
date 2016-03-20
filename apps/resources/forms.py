__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from ..common.forms.mixins import PagedForm
from ..work.models import LabourType
from .models import Employee, Equipment, EquipmentType


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


class EquipmentTypeForm(OwnedEntityForm):

    class Meta:
        model = EquipmentType
        exclude = ('owner', 'labour_types',)

    et_labour_types = forms.ModelMultipleChoiceField(queryset=LabourType.objects.all(),
                                                     required=False, label='Labour types')
    parent = forms.ModelChoiceField(queryset=EquipmentType.objects.filter(parent=None),
                                    required=False)

    def __init__(self, *args, **kwargs):
        super(EquipmentTypeForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            f = self.fields['et_labour_types']
            f.initial = self.instance.get_labour_types_for(self.user)

    def save(self, *args, **kwargs):
        et = super(EquipmentTypeForm, self).save(*args, **kwargs)

        # Update labour types, first remove and then add
        lts = self.cleaned_data['et_labour_types']
        et.update_labour_types(lts, self.user)

        # Return saved instance
        return et


class EmployeeSearchForm(ModernForm, PagedForm):
    identifier = forms.CharField(max_length=16, required=False, label='Employee identifier')
    name = forms.CharField(max_length=32, required=False, label='Employee name')

    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)


class EquipmentSearchForm(ModernForm, PagedForm):
    identifier = forms.CharField(max_length=16, required=False, label='Equipment identifier')
    type = forms.CharField(max_length=32, required=False, label='Equipment type')

    def __init__(self, *args, **kwargs):
        super(EquipmentSearchForm, self).__init__(*args, **kwargs)


class EquipmentTypeSearchForm(ModernForm, PagedForm):
    name__icontains = forms.CharField(max_length=32, required=False, label='Type name')

