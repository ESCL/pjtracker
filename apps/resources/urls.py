__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .api.resources import EmployeesResource, EquipmentResource
from .views import EmployeeView, EquipmentView, EquipmentTypeView, ResourceCategoryView


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

    # Equipment type views
    url(r'^equipment-types/$', EquipmentTypeView.as_view(), name='equipment-types'),
    url(r'^equipment-types/(?P<action>add)/$', EquipmentTypeView.as_view(), name='equipment-type'),
    url(r'^equipment-types/(?P<pk>\d+)/$', EquipmentTypeView.as_view(), name='equipment-type'),
    url(r'^equipment-types/(?P<pk>\d+)/(?P<action>edit)/$', EquipmentTypeView.as_view(), name='equipment-type'),

    # Resource categories
    url(r'^categories/$', ResourceCategoryView.as_view(), name='resource-categories'),
    url(r'^categories/(?P<action>add)/$', ResourceCategoryView.as_view(), name='resource-category'),
    url(r'^categories/(?P<pk>\d+)/$', ResourceCategoryView.as_view(), name='resource-category'),
    url(r'^categories/(?P<pk>\d+)/(?P<action>edit)/$', ResourceCategoryView.as_view(), name='resource-category'),

    # APIs
    url('^api/', include(api_v0.urls))
]
