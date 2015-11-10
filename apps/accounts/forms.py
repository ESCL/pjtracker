__author__ = 'kako'


from .models import User
from ..common.forms import OwnedEntityForm


class UserForm(OwnedEntityForm):

    class Meta:
        model = User
        fields = ('username',)

