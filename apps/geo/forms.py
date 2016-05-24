__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntitiesForm, OwnedEntityForm
from .models import Location


class LocationSearchForm(OwnedEntitiesForm):
    """
    Search form for location list.
    """
    name__icontains = forms.CharField(min_length=4, max_length=32, required=False, label='Location name')


class LocationForm(OwnedEntityForm):
    """
    Edit form for location instance.
    """
    class Meta:
        model = Location
        exclude = ('owner',)
