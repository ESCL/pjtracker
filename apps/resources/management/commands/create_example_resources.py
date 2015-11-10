__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....organizations.models import Team
from ....work.models import Project
from ...factories import EmployeeFactory, EquipmentFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Creating example resources...")
        pj = Project.objects.get()
        res = []

        # Fetch teams
        eng_team, cst_team = Team.objects.all()

        # Create resources for eng team
        res.append(EmployeeFactory.create(team=eng_team, project=pj))
        res.append(EmployeeFactory.create(team=eng_team, project=pj))

        # Create resources for cst team
        res.append(EmployeeFactory.create(team=cst_team, project=pj))
        res.append(EmployeeFactory.create(team=cst_team, project=pj))
        res.append(EquipmentFactory.create(team=cst_team, project=pj))

        # Done, print resources
        print("Created resources {}.".format(res))


