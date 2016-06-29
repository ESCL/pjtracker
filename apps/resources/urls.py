__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .api.resources import EmployeesResource, EquipmentResource
from .views import (EmployeeView, EquipmentView, EquipmentTypeView, ResourceCategoryView,
                    ResourceProjectAssignmentView, ResourceProjectAssignmentActionView)


api_v0 = Api(api_name='v0')
api_v0.register(EmployeesResource())
api_v0.register(EquipmentResource())

employee_view = EmployeeView.as_view()
equipment_view = EquipmentView.as_view(collection_view_name='equipments')
equipment_type_view = EquipmentTypeView.as_view(collection_view_name='equipment-types')
resource_category_view = ResourceCategoryView.as_view(collection_view_name='resource-categories')

employees_project_view = ResourceProjectAssignmentView.as_view(
    views={'parent_collection': 'employees',
           'parent_instance': 'employee',
           'collection': 'employee-projects',
           'instance': 'employee-project',
           'action': 'employee-project-action'},
    collection_view_name='employee-projects'
)
equipment_project_view = ResourceProjectAssignmentView.as_view(
    views={'parent_collection': 'equipments',
           'parent_instance': 'equipment',
           'collection': 'equipment-projects',
           'instance': 'equipment-project',
           'action': 'equipment-project-action'},
    collection_view_name='equipment-projects'
)

employee_project_action_view = ResourceProjectAssignmentActionView.as_view(
    views={'parent_collection': 'employees',
           'parent_instance': 'employee',
           'collection': 'employee-projects',
           'instance': 'employee-project',
           'action': 'employee-project-action'},
    collection_view_name='employee-projects'
)
equipment_project_action_view = ResourceProjectAssignmentActionView.as_view(
    views={'parent_collection': 'equipments',
           'parent_instance': 'equipment',
           'collection': 'equipment-projects',
           'instance': 'equipment-project',
           'action': 'equipment-project-action'},
    collection_view_name='equipment-projects'
)


urlpatterns = [
    # Employee view
    url(r'^employees/$', employee_view, name='employees'),
    url(r'^employees/(?P<action>add)/$', employee_view, name='employee'),
    url(r'^employees/(?P<pk>\d+)/$', employee_view, name='employee'),
    url(r'^employees/(?P<pk>\d+)/(?P<action>edit)/$', employee_view, name='employee'),

    # Employee project assignment
    url(r'^employees/(?P<parent_pk>\d+)/projects/$', employees_project_view, name='employee-projects'),
    url(r'^employees/(?P<parent_pk>\d+)/projects/(?P<action>add)/$', employees_project_view, name='employee-project'),
    url(r'^employees/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/$', employees_project_view, name='employee-project'),
    url(r'^employees/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/(?P<action>edit)/$', employees_project_view, name='employee-project'),

    # Employee project assignment action
    url(r'^employees/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/actions/$', employee_project_action_view,
        {'action': 'add'}, name='employee-project-action'),

    # Equipment view
    url(r'^equipments/$', equipment_view, name='equipments'),
    url(r'^equipments/(?P<action>add)/$', equipment_view, name='equipment'),
    url(r'^equipments/(?P<pk>\d+)/$', equipment_view, name='equipment'),
    url(r'^equipments/(?P<pk>\d+)/(?P<action>edit)/$', equipment_view, name='equipment'),

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

    # Equipment project assignment
    url(r'^equipments/(?P<parent_pk>\d+)/projects/$', equipment_project_view, name='equipment-projects'),
    url(r'^equipments/(?P<parent_pk>\d+)/projects/(?P<action>add)/$', equipment_project_view, name='equipment-project'),
    url(r'^equipments/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/$', equipment_project_view, name='equipment-project'),
    url(r'^equipments/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/(?P<action>edit)/$', equipment_project_view, name='equipment-project'),

    # Equipment project assignment action
    url(r'^equipments/(?P<parent_pk>\d+)/projects/(?P<pk>\d+)/actions/$', equipment_project_action_view,
        {'action': 'add'}, name='equipment-project-action'),

    # APIs
    url('^api/', include(api_v0.urls))
]
