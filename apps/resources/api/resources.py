__author__ = 'kako'

from tastypie.resources import ModelResource

from ..models import Employee, Equipment


class EmployeesResource(ModelResource):

    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employees'


class EquipmentResource(ModelResource):

    class Meta:
        queryset = Equipment.objects.all()
        resource_name = 'equipment'