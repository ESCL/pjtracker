__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .api.resources import EmployeesResource, EquipmentResource
from .views import EmployeeView, EquipmentView


api_v0 = Api(api_name='v0')
api_v0.register(EmployeesResource())
api_v0.register(EquipmentResource())


urlpatterns = [
    # Employee view
    url(r'^employees/$', EmployeeView.as_view(), name='employees'),
    url(r'^employees/(?P<action>add)/$', EmployeeView.as_view(), name='employee'),
    url(r'^employees/(?P<pk>\d+)/$', EmployeeView.as_view(), name='employee'),
    url(r'^employees/(?P<pk>\d+)/(?P<action>edit)/$', EmployeeView.as_view(), name='employee'),

    # Equipment view
    url(r'^equipment/$', EquipmentView.as_view(), name='equipments'),
    url(r'^equipment/(?P<action>add)/$', EquipmentView.as_view(), name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/$', EquipmentView.as_view(), name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/(?P<action>edit)/$', EquipmentView.as_view(), name='equipment'),

    # APIs
    url('^api/', include(api_v0.urls))
]
