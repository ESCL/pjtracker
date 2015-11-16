__author__ = 'kako'

from tastypie import resources

from ...common.api.resources import OwnedResource

from ..models import Employee, Equipment


class EmployeesResource(OwnedResource):

    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employees'
        fields = ('identifier', 'first_name', 'last_name',)


class EquipmentResource(OwnedResource):

    class Meta:
        queryset = Equipment.objects.all()
        resource_name = 'equipment'
        fields = ('identifier', 'model', 'year',)

