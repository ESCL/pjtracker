__author__ = 'kako'

from ..common.forms import OwnedEntityForm
from .models import Company, Team


class CompanyForm(OwnedEntityForm):

    class Meta:
        model = Company
        exclude = ('owner',)


class TeamForm(OwnedEntityForm):

    class Meta:
        model = Team
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        # Restrict activities to workable only
        f = self.fields['activities']
        f.queryset = f.queryset.workable()
