__author__ = 'kako'

from django.db.models import Q

from ..common.db.query import OwnedEntityQuerySet


class EmployeeQuerySet(OwnedEntityQuerySet):

    def filter(self, *args, **kwargs):
        args = list(args)
        name = kwargs.pop('name', None)
        if name:
            args.append(Q(Q(first_name__icontains=name)|Q(last_name__icontains=name)))

        return super(EmployeeQuerySet, self).filter(*args, **kwargs)


class EquipmentQuerySet(OwnedEntityQuerySet):

    def filter(self, *args, **kwargs):
        args = list(args)
        type = kwargs.pop('type', None)
        if type:
            args.append(Q(Q(type__name__icontains=type)|Q(type__parent__name__icontains=type)))

        return super(EquipmentQuerySet, self).filter(*args, **kwargs)


class ResourceProjectAssignmentQuerySet(OwnedEntityQuerySet):

    def in_dates(self, start, end):
        qs = self.exclude(end_date__lt=start)
        if end:
            qs = qs.exclude(start_date__gt=end)
        return qs
