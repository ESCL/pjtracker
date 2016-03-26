__author__ = 'kako'

from datetime import datetime

from django_values_group import ValuesGroupMixin
from ..common.db.query import OwnedEntityQuerySet


class WorkLogQuerySet(ValuesGroupMixin, OwnedEntityQuerySet):

    def filter_for_querystring(self, querystring):
        """
        Apply a bunch of filters according to the passed querystring.
        """
        filters = {}
        ts_model = self.model.timesheet.field.rel.to

        # Add status filter if specified
        status = querystring.get('status')
        if status == 'approved':
            filters['timesheet__status'] = ts_model.STATUS_APPROVED
        elif status == 'issued':
            filters['timesheet__status'] = ts_model.STATUS_ISSUED

        # Add date range filters if specified
        date_start = querystring.get('from_date')
        date_end = querystring.get('to_date')
        if date_start:
            filters['timesheet__date__gte'] = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            filters['timesheet__date__lte'] = datetime.strptime(date_end, '%Y-%m-%d').date()

        # Add resource type filter if required
        res_type = querystring.get('resource_type')
        if res_type:
            filters['resource__resource_type'] = res_type

        # Apply all filters and return
        return self.filter(**filters)

    def group_by(self, main_groups):
        """
        Apply a bunch of group_bys according to the passed querystring.
        """
        groups = []

        # Default to grouping by project if no grouping is defined
        if not main_groups or 'project' in main_groups:
            groups.append('activity__project_id')

        # Check other grouping options
        if 'activity' in main_groups:
            groups.extend(('activity__id', 'activity__parent_id',
                           'activity__code', 'activity__name',
                           'activity__project_id',))
        if 'labour_type' in main_groups:
            groups.extend(('labour_type__id', 'labour_type__code',
                           'labour_type__name',))
        if 'resource' in main_groups:
            groups.extend(('resource__id', 'resource__identifier',
                           'resource__resource_type',))
        if 'date' in main_groups:
            groups.extend(('timesheet__id', 'timesheet__date',
                           'timesheet__status',))

        # Return grouped queryset (a ValuesGroupQuerySet)
        return self.values(*groups)
