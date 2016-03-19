__author__ = 'kako'

from django.forms import DateField


class ModernFieldsMixin(object):

    def modernize_fields(self):
        for k, field in self.fields.items():
            label = field.label or k.replace('_', '').title()
            if isinstance(field, DateField):
                field.widget.attrs['title'] = label
                field.widget.input_type = 'date'
            else:
                field.widget.attrs['title'] = label
                field.widget.attrs['placeholder'] = label


class RestrictedQuerySetsMixin(object):

    def restrict_querysets(self):
        """
        Restrict queryset in all fields for the given user.
        """
        for field in self.fields.values():
            if hasattr(field, 'queryset'):
                if hasattr(field.queryset, 'for_user'):
                    field.queryset = field.queryset.for_user(self.user)

