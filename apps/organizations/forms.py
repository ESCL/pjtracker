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
