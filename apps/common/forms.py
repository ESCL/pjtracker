__author__ = 'kako'

from django import forms


class OwnedEntityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(OwnedEntityForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Make user account owner it object is new
        if self.instance.id is None:
            self.instance.owner = self._user.profile.account

        return super(OwnedEntityForm, self).save(*args, **kwargs)

