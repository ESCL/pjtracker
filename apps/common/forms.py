__author__ = 'kako'

from django import forms


class ModernizeFieldsMixin(object):

    def modernize_fields(self):
        for k, field in self.fields.items():
            label = field.label or k.replace('_', '').title()
            if isinstance(field, forms.DateField):
                field.widget.attrs['title'] = label
                field.widget.input_type = 'date'
            else:
                field.widget.attrs['title'] = label
                field.widget.attrs['placeholder'] = label


class ModernForm(ModernizeFieldsMixin, forms.Form):
    page_size = forms.IntegerField(required=False, label='Page size',
                                   min_value=10, max_value=50)

    def __init__(self, *args, **kwargs):
        super(ModernForm, self).__init__(*args, **kwargs)
        self.modernize_fields()
        self.fields['page_size'].widget.attrs['step'] = 10


class OwnedEntityForm(ModernizeFieldsMixin, forms.ModelForm):
    """
    Base model form for OwnedEntity subclasses, providing automatic disabled
    fields based on permissions, filters for choice fields based on user account
    (owner of instances) and HTML5 widgets.

    IMPORTANT: Only fields belonging to the model are disabled by default,
    so any extra fields added to the form MUST BE handled by the form itself,
    since they have no side effects by default anyway.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

        # First set the owner right away if it's a new instance
        # Note: restrict_fields is simplifier if we set it here
        if not self.instance.id:
            self.instance.owner = self.user.owner

        self.restrict_fields()
        self.restrict_querysets()
        self.modernize_fields()

    def restrict_fields(self):
        """
        Disable or remove fields for data that the user is not allowed to
        modify.
        """
        # Note: instance is always set, even if it's new
        disallowed_fields = self.user.get_disallowed_fields_for(self.instance)

        if self.is_bound:
            # Bound form, remove fields to allow submitting partial data
            for k in disallowed_fields:
                self.fields.pop(k, None)

        else:
            # Unbound form, disable them only but render them
            for k in disallowed_fields:
                f = self.fields.get(k)
                if f:
                    f.widget.attrs.update({'disabled': 'disabled',
                                           'readonly': True})

    def restrict_querysets(self):
        """
        Restrict queryset in all fields for the given user.
        """
        for field in self.fields.values():
            if hasattr(field, 'queryset'):
                if hasattr(field.queryset, 'for_user'):
                    field.queryset = field.queryset.for_user(self.user)

