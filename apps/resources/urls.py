__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .api.resources import EmployeesResource, EquipmentResource
from .views import EmployeeView, EquipmentView, EquipmentTypeView, ResourceCategoryView


api_v0 = Api(api_name='v0')
api_v0.register(EmployeesResource())
api_v0.register(EquipmentResource())

employee_view = EmployeeView.as_view()
equipment_view = EquipmentView.as_view(collection_view_name='equipments')
equipment_type_view = EquipmentTypeView.as_view(collection_view_name='equipment-types')
resource_category_view = ResourceCategoryView.as_view(collection_view_name='resource-categories')


urlpatterns = [
    # Employee view
    url(r'^employees/$', employee_view, name='employees'),
    url(r'^employees/(?P<action>add)/$', employee_view, name='employee'),
    url(r'^employees/(?P<pk>\d+)/$', employee_view, name='employee'),
    url(r'^employees/(?P<pk>\d+)/(?P<action>edit)/$', employee_view, name='employee'),

    # Equipment view
    url(r'^equipment/$', equipment_view, name='equipments'),
    url(r'^equipment/(?P<action>add)/$', equipment_view, name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/$', equipment_view, name='equipment'),
    url(r'^equipment/(?P<pk>\d+)/(?P<action>edit)/$', equipment_view, name='equipment'),

    # Equipment type views
    url(r'^equipment-types/$', equipment_type_view, name='equipment-types'),
    url(r'^equipment-types/(?P<action>add)/$', equipment_type_view, name='equipment-type'),
    url(r'^equipment-types/(?P<pk>\d+)/$', equipment_type_view, name='equipment-type'),
    url(r'^equipment-types/(?P<pk>\d+)/(?P<action>edit)/$', equipment_type_view, name='equipment-type'),

    # Resource categories
    url(r'^categories/$', resource_category_view, name='resource-categories'),
    url(r'^categories/(?P<action>add)/$', resource_category_view, name='resource-category'),
    url(r'^categories/(?P<pk>\d+)/$', resource_category_view, name='resource-category'),
    url(r'^categories/(?P<pk>\d+)/(?P<action>edit)/$', resource_category_view, name='resource-category'),

    # APIs
    url('^api/', include(api_v0.urls))
]
