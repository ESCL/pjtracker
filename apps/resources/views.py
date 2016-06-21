
from ..common.views.base import StandardResourceView
from .models import (Employee, Equipment, EquipmentType, ResourceCategory,
                     ResourceProjectAssignment)
from .forms import (EmployeeForm, EmployeeSearchForm, EquipmentForm,
                    EquipmentSearchForm, EquipmentTypeForm, EquipmentTypeSearchForm,
                    ResourceCategoryForm, ResourceCategorySearchForm)


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
    # Override collection view name to incorrect plural
    collection_view_name = 'equipments'


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
    # Override default to make it "sluggish"
    collection_view_name = 'equipment-types'


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
    # Override default to make it "sluggish"
    collection_view_name = 'resource-categories'
