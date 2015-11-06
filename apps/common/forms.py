__author__ = 'kako'

from django import forms


class ModernizeFieldsMixin(object):

    def modernize_fields(self):
        for field in self.fields.values():
            if isinstance(field, forms.DateField):
                field.widget.input_type = 'date'


class OwnedEntityForm(forms.ModelForm, ModernizeFieldsMixin):

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

        if self._user:
            self._restrict_querysets()
        self.modernize_fields()

    def _restrict_querysets(self):
        """
        Restrict queryset in all fields for the given user.
        :return:
        """
        for field in self.fields.values():
            if hasattr(field, 'queryset'):
                if hasattr(field.queryset, 'for_user'):
                    field.queryset = field.queryset.for_user(self._user)

    def save(self, *args, **kwargs):
        # Make user account owner if object is new
        if self.instance.id is None and hasattr(self._user, 'profile'):
            self.instance.owner = self._user.profile.account

        return super(OwnedEntityForm, self).save(*args, **kwargs)
