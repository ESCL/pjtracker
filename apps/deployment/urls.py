__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .views import TimeSheetView, TimeSheetActionView, HoursView
from .api.resources import HoursResource


timesheet_view = TimeSheetView.as_view()
timesheet_action_view = TimeSheetActionView.as_view()
hours_view = HoursView.as_view()

api = Api(api_name='v0')
api.register(HoursResource())

urlpatterns = [
    # Timesheet view
    url(r'^timesheets/$', timesheet_view, name='timesheets'),
    url(r'^timesheets/(?P<action>add)/$', timesheet_view, name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/$', timesheet_view, name='timesheet'),
    url(r'^timesheets/(?P<pk>\d+)/(?P<action>edit)/$', timesheet_view, name='timesheet'),

    # Timesheet action view
    url(r'^timesheets/(?P<pk>\d+)/actions/$', timesheet_action_view, {'action': 'add'}, name='timesheet-action'),

    # Hours summary view
    url(r'^hours/$', hours_view, name='hours'),

    # APIs
    url(r'^api/', include(api.urls)),
]
