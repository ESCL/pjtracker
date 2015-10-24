__author__ = 'kako'

from django.forms import ModelForm

from .models import Employee


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        exclude = ()