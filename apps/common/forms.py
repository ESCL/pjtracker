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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

        # Execute all required field modifications
        self.restrict_fields()
        self.restrict_querysets()
        self.modernize_fields()

    def restrict_fields(self):
        """
        Disable or remove fields for data that the user is not allowed to
        modify.
        """
        # Note: instance is always set, even if it's new
        allowed_fields = set(self.user.get_allowed_fields_for(self.instance))

        if self.is_bound:
            # Bound form, remove fields to allow submitting partial data
            for k in list(self.fields.keys()):
                if k not in allowed_fields:
                    self.fields.pop(k)

        else:
            # Unbound form, disable them only but render them
            for k, field in self.fields.items():
                if k not in allowed_fields:
                    field.widget.attrs.update({'disabled': 'disabled', 'readonly': True})

    def restrict_querysets(self):
        """
        Restrict queryset in all fields for the given user.
        """
        for field in self.fields.values():
            if hasattr(field, 'queryset'):
                if hasattr(field.queryset, 'for_user'):
                    field.queryset = field.queryset.for_user(self.user)

    def save(self, *args, **kwargs):
        # Make user account owner if object is new
        if not self.instance.id:
            self.instance.owner = self.user.owner

        return super(OwnedEntityForm, self).save(*args, **kwargs)
