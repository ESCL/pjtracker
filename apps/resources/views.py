
from ..common.views.base import StandardResourceView
from .models import Employee, Equipment, EquipmentType
from .forms import EmployeeForm, EmployeeSearchForm, EquipmentForm, EquipmentSearchForm, EquipmentTypeForm, EquipmentTypeSearchForm


class EmployeeView(StandardResourceView):
    model = Employee
    list_template = 'employees.html'
    detail_template = 'employee.html'
    edit_template = 'employee-edit.html'
    main_form = EmployeeForm
    search_form = EmployeeSearchForm


class EquipmentView(StandardResourceView):
    model = Equipment
    list_template = 'equipments.html'
    detail_template = 'equipment.html'
    edit_template = 'equipment-edit.html'
    main_form = EquipmentForm
    search_form = EquipmentSearchForm
    # Override collection view name to incorrect plural
    collection_view_name = 'equipments'


class EquipmentTypeView(StandardResourceView):
    model = EquipmentType
    list_template = 'equipment-types.html'
    detail_template = 'equipment-type.html'
    edit_template = 'equipment-type-edit.html'
    main_form = EquipmentTypeForm
    search_form = EquipmentTypeSearchForm
    # Override default to make it "sluggish"
    collection_view_name = 'equipment-types'
