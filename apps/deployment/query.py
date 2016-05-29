__author__ = 'kako'

from datetime import datetime

from django_group_by import GroupByMixin
from ..common.db.query import OwnedEntityQuerySet


class WorkLogQuerySet(OwnedEntityQuerySet, GroupByMixin):

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

    def group_for_querystring(self, main_groups):
        """
        Apply a bunch of group_bys according to the passed querystring.
        """
        groups = []

        # Default to grouping by project if no grouping is defined
        if not main_groups or 'project' in main_groups:
            groups.append('activity__project')

        # Check other grouping options
        if 'activity' in main_groups:
            groups.append('activity')
        if 'labour_type' in main_groups:
            groups.append('labour_type')
        if 'resource' in main_groups:
            groups.append('resource')
        if 'date' in main_groups:
            groups.append('timesheet')

        # Return grouped queryset (a ValuesGroupQuerySet)
        return self.group_by(*groups)
