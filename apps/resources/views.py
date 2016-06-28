
from ..common.views.base import StandardResourceView, SubResourceView
from ..deployment.models import ResourceProjectAssignment
from .models import (Employee, Equipment, EquipmentType, ResourceCategory, Resource)
from .forms import (EmployeeForm, EmployeeSearchForm, EquipmentForm,
                    EquipmentSearchForm, EquipmentTypeForm, EquipmentTypeSearchForm,
                    ResourceCategoryForm, ResourceCategorySearchForm,
                    ResourceProjectAssignmentForm, ResourceProjectAssignmentSearchForm,
                    ResourceProjectAssignmentActionForm)


class EmployeeView(StandardResourceView):
    model = Employee
    list_template = 'employees.html'
    detail_template = 'employee.html'
    edit_template = 'employee-edit.html'
    main_form = EmployeeForm
    search_form = EmployeeSearchForm
    permissions = {
        'add': ('resources.add_employee',),
        'edit': ('resources.change_employee',)
    }


class EquipmentView(StandardResourceView):
    model = Equipment
    list_template = 'equipments.html'
    detail_template = 'equipment.html'
    edit_template = 'equipment-edit.html'
    main_form = EquipmentForm
    search_form = EquipmentSearchForm
    permissions = {
        'add': ('resources.add_equipment',),
        'edit': ('resources.change_equipment',)
    }


class EquipmentTypeView(StandardResourceView):
    model = EquipmentType
    list_template = 'equipment-types.html'
    detail_template = 'equipment-type.html'
    edit_template = 'equipment-type-edit.html'
    main_form = EquipmentTypeForm
    search_form = EquipmentTypeSearchForm
    permissions = {
        'add': ('resources.add_equipmenttype',),
        'edit': ('resources.change_equipmenttype',)
    }


class ResourceCategoryView(StandardResourceView):
    model = ResourceCategory
    list_template = 'resource-categories.html'
    detail_template = 'resource-category.html'
    edit_template = 'resource-category-edit.html'
    main_form = ResourceCategoryForm
    search_form = ResourceCategorySearchForm
    permissions = {
        'add': ('resources.add_resourcecategory',),
        'edit': ('resources.change_resourcecategory',),
    }


class ResourceProjectAssignmentView(SubResourceView):
    parent_model = Resource
    parent_attr = 'resource'
    model = ResourceProjectAssignment
    list_template = 'resource-projects.html'
    detail_template = 'resource-project.html'
    edit_template = 'resource-project-edit.html'
    main_form = ResourceProjectAssignmentForm
    search_form = ResourceProjectAssignmentSearchForm
    permissions = {
        'add': ('deployment.add_resourceprojectassignment',),
        'edit': ('deployment.change_resourceprojectassignment',)
    }


class ResourceProjectAssignmentActionView(SubResourceView):
    parent_model = Resource
    parent_attr = 'resource'
    model = ResourceProjectAssignment
    edit_template = 'resource-project-action.html'
    main_form = ResourceProjectAssignmentActionForm
    permissions = {
        'add': ('deployment.issue_resourceprojectassignment',
                'deployment.review_resourceprojectassignment',)
    }
