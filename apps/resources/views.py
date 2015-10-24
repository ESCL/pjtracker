from django.shortcuts import render

from ..common.views import StandardResourceView
from .models import Employee
from .forms import EmployeeForm


class EmployeeView(StandardResourceView):
    list_template = 'employees.html'
    detail_template = 'employee.html'
    edit_template = 'form.html'
    edit_form = EmployeeForm
    model = Employee
