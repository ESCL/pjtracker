__author__ = 'kako'


from django import forms

from ..common.forms import OwnedEntityForm, OwnedEntitiesForm
from ..work.models import LabourType
from .models import (Employee, Equipment, EquipmentType, ResourceCategory,
                     ResourceProjectAssignment,)


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


class ResourceProjectAssignmentSearchForm(OwnedEntitiesForm):
    resource__identifier__icontains = forms.CharField(max_length=8, required=False, label='Employee/Equipment code')
    project__code__icontains = forms.CharField(max_length=6, required=False, label='Project code')


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


class ResourceProjectAssignmentForm(OwnedEntityForm):

    class Meta:
        model = ResourceProjectAssignment
        exclude = ('owner', 'resource', 'timestamp', 'status',)

    def __init__(self, *args, **kwargs):
        # Pop and store parent before init
        self.resource = kwargs.pop('parent')
        super(ResourceProjectAssignmentForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Clean all inter-dependent fields.
        """
        # Get cleaned data
        cleaned_data = super(ResourceProjectAssignmentForm, self).clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        # Validate dates by comparison
        if end and end < start:
            self.add_error('end_date', forms.ValidationError('End date cannot be less than start date.'))

        # Validate dates by collisions (issued and approved assignments)
        if start:
            collisions = ResourceProjectAssignment.objects.filter(
                resource=self.resource,
                status__in=(ResourceProjectAssignment.STATUS_APPROVED,
                            ResourceProjectAssignment.STATUS_ISSUED)
            ).in_dates(start, end)
            if collisions.exists():
                self.add_error(None, forms.ValidationError('Date range collides with other assignments.'))

        # Return cleaned data
        return cleaned_data

    def save(self, *args, **kwargs):
        """
        Save resource project assignment instance.
        """
        # Set resource (from parent)
        self.instance.resource = self.resource

        # Finally, save instance
        return super(ResourceProjectAssignmentForm, self).save(*args, **kwargs)


class ResourceProjectAssignmentActionForm(forms.Form):
    """
    Form for creating a ResourceProjectAssignmentAction instance.
    """
    action = forms.ChoiceField()
    feedback = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        # Pop and store user+assignment
        self.user = kwargs.pop('user', None)
        self.resource = kwargs.pop('parent', None)
        self.assignment = kwargs.pop('instance', None)

        # Init form
        super(ResourceProjectAssignmentActionForm, self).__init__(*args, **kwargs)

        # Add choices to actions based on current status
        self.fields['action'].choices = self.assignment.allowed_actions

    def clean(self):
        """
        Clean inter-dependent field values.
        """
        # Get cleaned data
        cleaned_data = super(ResourceProjectAssignmentActionForm, self).clean()
        action = cleaned_data.get('action')
        feedback = cleaned_data.get('feedback')

        # Validate status+feedback
        if action == 'reject' and not feedback:
            self.add_error('feedback', forms.ValidationError('This field is required for rejections.'))

        # Validate for approval
        if action == 'approve':
            # Make sure there are no collisions
            # TODO: Make sure we really need this check here, we're already validating on creation
            collisions = ResourceProjectAssignment.objects.filter(
                resource=self.assignment.resource,
                status__in=(ResourceProjectAssignment.STATUS_APPROVED,
                            ResourceProjectAssignment.STATUS_ISSUED)
            ).exclude(
                id=self.assignment.id
            ).in_dates(
                self.assignment.start_date,
                self.assignment.end_date
            )
            if collisions.exists():
                self.add_error(None, forms.ValidationError('Date range collides with other assignments.'))

        # Return cleaned data
        return cleaned_data

    def save(self):
        # Determine method and execute it
        action = self.cleaned_data.get('action')
        method = getattr(self.assignment, action)
        method(self.user)
