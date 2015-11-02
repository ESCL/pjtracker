__author__ = 'kako'


from django import forms

from .db.models import OwnedEntity


class OwnedEntityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if isinstance(self.instance, OwnedEntity):
            self.instance.owner = self._user.profile.account
        return super(OwnedEntityForm, self).save(*args, **kwargs)

