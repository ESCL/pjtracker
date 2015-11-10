__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
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


class CompanySearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Company code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Company name')


class TeamSearchForm(ModernForm):
    code__iexact = forms.CharField(max_length=16, required=False, label='Team code')
    name__icontains = forms.CharField(max_length=32, required=False, label='Team name')
    company__code__iexact = forms.CharField(max_length=32, required=False, label='Company')
