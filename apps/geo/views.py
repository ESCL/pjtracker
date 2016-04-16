
from ..common.views.base import StandardResourceView
from .forms import LocationSearchForm, LocationForm
from .models import Location


class LocationView(StandardResourceView):
    model = Location
    list_template = 'locations.html'
    detail_template = 'location.html'
    edit_template = 'location-edit.html'
    search_form = LocationSearchForm
    main_form = LocationForm
    permissions = {
        'add': ('geo.add_location',),
        'edit': ('geo.change_location',)
    }
