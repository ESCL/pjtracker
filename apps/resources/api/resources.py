__author__ = 'kako'

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ..models import Employee, Equipment


class EmployeesResource(OwnedResource):

    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employees'
        fields = ('identifier', 'first_name', 'last_name',)
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=['json', 'csv'])


class EquipmentResource(OwnedResource):

    class Meta:
        queryset = Equipment.objects.all()
        resource_name = 'equipment'
        fields = ('identifier', 'model', 'year',)
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=['json', 'csv'])

