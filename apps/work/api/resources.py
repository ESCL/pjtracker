__author__ = 'kako'

from tastypie import fields

from ...common.api.resources import OwnedResource
from ...common.api.serializers import JsonCsvSerializer
from ..models import Activity


class ActivityResource(OwnedResource):

    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        fields = ('wbs_code', 'name', 'labour_types_codes', 'groups_codes',)
        include_resource_uri = False
        serializer = JsonCsvSerializer(formats=['json', 'csv'])

    wbs_code = fields.CharField(attribute='wbs_code')
    labour_types_codes = fields.CharField(attribute='labour_types_codes')
    groups_codes = fields.CharField(attribute='groups_codes')

    def apply_filters(self, request, applicable_filters):
        qs = super(ActivityResource, self).apply_filters(request, applicable_filters)

        active_only = request.GET.get('active_only')
        if active_only:
            qs = qs.workable()

        return qs