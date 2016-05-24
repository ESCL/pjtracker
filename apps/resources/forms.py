__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, OwnedEntitiesForm
from ..work.models import LabourType
from .models import Employee, Equipment, EquipmentType, ResourceCategory


class EmployeeSearchForm(OwnedEntitiesForm):
    identifier = forms.CharField(max_length=16, required=False, label='Employee identifier')
    name = forms.CharField(max_length=32, required=False, label='Employee name')


class EquipmentSearchForm(OwnedEntitiesForm):
    identifier = forms.CharField(max_length=16, required=False, label='Equipment identifier')
    type__code__icontains = forms.CharField(max_length=32, required=False, label='Equipment type')


class EquipmentTypeSearchForm(OwnedEntitiesForm):
    code__icontains = forms.CharField(max_length=8, required=False, label='Type code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Type name')


class ResourceCategorySearchForm(OwnedEntitiesForm):
    code__icontains = forms.CharField(max_length=8, required=False, label='Category code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Category name')


class ResourceFormBase(OwnedEntityForm):
    """
    Base class for all resource model forms, providing common functionality
    to filter querysets in model choice fields.
    """
    def __init__(self, *args, **kwargs):
        super(ResourceFormBase, self).__init__(*args, **kwargs)
        cat = self.fields['category']
        cat.queryset = cat.queryset.filter(resource_type__in=('all', self.Meta.model._meta.model_name))


class EmployeeForm(ResourceFormBase):

    class Meta:
        model = Employee
        # Team assignment is managed in team form
        exclude = ('owner', 'resource_type', 'team',)


class EquipmentForm(ResourceFormBase):

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


class ResourceCategoryForm(OwnedEntityForm):

    class Meta:
        model = ResourceCategory
        exclude = ('owner',)
