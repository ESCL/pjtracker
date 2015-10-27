
from ..common.views.base import StandardResourceView
from .models import Employee, Equipment
from .forms import EmployeeForm


class EmployeeView(StandardResourceView):
    list_template = 'employees.html'
    detail_template = 'employee.html'
    edit_template = 'form.html'
    edit_form = EmployeeForm
    model = Employee


class EquipmentView(StandardResourceView):
    list_template = 'equipment.html'
    detail_template = 'equipment.html'
    edit_template = 'form.html'
    edit_form = EmployeeForm
    model = Equipment
