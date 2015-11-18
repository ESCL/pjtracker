__author__ = 'kako'

from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ..models import Activity, Project


class ActivityResource(OwnedResource):

    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        fields = ('wbs_code', 'name', 'labour_types', 'groups',)
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=['json', 'csv'])

    wbs_code = fields.CharField(attribute='full_wbs_code')
    labour_types = fields.CharField(attribute='labour_types_codes')
    groups = fields.CharField(attribute='groups_codes')

    def apply_filters(self, request, applicable_filters):
        """
        Add "active" filter.
        """
        qs = super(ActivityResource, self).apply_filters(request, applicable_filters)
        if 'active' in request.GET:
            qs = qs.workable()
        return qs


class ProjectResource(OwnedResource):

    class Meta:
        queryset = Project.objects.all()
        resource_name = 'projects'
        fields = ('code', 'name', 'employees', 'equipment')
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=['json', 'csv'])

    employees = fields.IntegerField(attribute='employees_count')
    equipment = fields.IntegerField(attribute='equipment_count')
