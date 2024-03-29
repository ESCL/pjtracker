__author__ = 'kako'

from django import forms

from .mixins import ModernFieldsMixin, RestrictedQuerySetsMixin


class OwnedEntitiesForm(ModernFieldsMixin, RestrictedQuerySetsMixin, forms.Form):
    """
    Base model for all non-model forms with restricted querysets and HTML5
    widgets for their fields.
    """
    def __init__(self, *args, **kwargs):
        super(OwnedEntitiesForm, self).__init__(*args, **kwargs)
        self.restrict_querysets()
        self.modernize_fields()


class OwnedEntityForm(ModernFieldsMixin, RestrictedQuerySetsMixin, forms.ModelForm):
    """
    Base model form for OwnedEntity subclasses, providing automatic disabled
    fields based on permissions, filters for choice fields based on user account
    (owner of instances) and HTML5 widgets.

    IMPORTANT: Only fields belonging to the model are disabled by default,
    so any extra fields added to the form MUST BE handled by the form itself,
    since they have no side effects by default anyway.
    """
    def __init__(self, *args, **kwargs):
        """
        Set owner to new insstance, restrict fields, querysets and
        modernize fields.
        """
        # Note: super sets "user" attribute (RestrictedQuerySetMixin does it)
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

        # First set the owner right away if it's a new instance
        # Note: restrict_fields is simplified if we set it here
        if not self.instance.id:
            self.instance.owner = self.user.owner

        # Prepare the form fields and their querysets
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
