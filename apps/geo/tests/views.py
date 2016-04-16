
from django.test import TestCase

from ...common.test import PermissionTestMixin
from ..factories import LocationFakeFactory
from ..models import Location


class LabourTypeViewTest(PermissionTestMixin, TestCase):
    model = Location
    model_factory = LocationFakeFactory
    list_view_name = 'locations'
    instance_view_name = 'location'
