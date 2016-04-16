__author__ = 'claudio.melendrez'

from django.test import TestCase

from ...common.test import PermissionTestMixin
from ..factories import CompanyFactory, DepartmentFactory, PositionFactory, TeamFactory
from ..models import Company, Department, Position, Team


class CompanyViewTest(PermissionTestMixin, TestCase):
    model = Company
    model_factory = CompanyFactory
    list_view_name = 'companies'
    instance_view_name = 'company'


class DepartmentViewTest(PermissionTestMixin, TestCase):
    model = Department
    model_factory = DepartmentFactory
    list_view_name = 'departments'
    instance_view_name = 'department'


class PositionViewTest(PermissionTestMixin, TestCase):
    model = Position
    model_factory = PositionFactory
    list_view_name = 'positions'
    instance_view_name = 'position'


class TeamViewTest(PermissionTestMixin, TestCase):
    model = Team
    model_factory = TeamFactory
    list_view_name = 'teams'
    instance_view_name = 'team'
    edit_perm = 'change activities'
