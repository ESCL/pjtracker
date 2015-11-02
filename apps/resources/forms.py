__author__ = 'kako'

from ..common.forms import OwnedEntityForm
from .models import Employee, Equipment


class EmployeeForm(OwnedEntityForm):

    class Meta:
        model = Employee
        exclude = ('owner',)



class EquipmentForm(OwnedEntityForm):

    class Meta:
        model = Equipment
        exclude = ('owner',)

