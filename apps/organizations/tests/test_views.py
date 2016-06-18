__author__ = 'claudio.melendrez'

from django.test import TestCase

from ...common.test import PermissionTestMixin
from ..factories import CompanyFakeFactory, DepartmentFakeFactory, PositionFakeFactory, TeamFakeFactory
from ..models import Company, Department, Position, Team


class CompanyViewTest(PermissionTestMixin, TestCase):
    model = Company
    model_factory = CompanyFakeFactory
    list_view_name = 'companies'
    instance_view_name = 'company'


class DepartmentViewTest(PermissionTestMixin, TestCase):
    model = Department
    model_factory = DepartmentFakeFactory
    list_view_name = 'departments'
    instance_view_name = 'department'


class PositionViewTest(PermissionTestMixin, TestCase):
    model = Position
    model_factory = PositionFakeFactory
    list_view_name = 'positions'
    instance_view_name = 'position'


class TeamViewTest(PermissionTestMixin, TestCase):
    model = Team
    model_factory = TeamFakeFactory
    list_view_name = 'teams'
    instance_view_name = 'team'
    edit_perm = 'change activities'
