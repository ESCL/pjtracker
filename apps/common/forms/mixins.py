__author__ = 'kako'

from django.forms import DateField, IntegerField


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


class PagedForm(object):
    page_size = IntegerField(required=False, label='Page size',
                             min_value=10, max_value=50)

    def __init__(self, *args, **kwargs):
        self.fields['page_size'].widget.attrs['step'] = 10


class RestrictedQuerySetsMixin(object):

    def restrict_querysets(self):
        """
        Restrict queryset in all fields for the given user.
        """
        for field in self.fields.values():
            if hasattr(field, 'queryset'):
                if hasattr(field.queryset, 'for_user'):
                    field.queryset = field.queryset.for_user(self.user)

