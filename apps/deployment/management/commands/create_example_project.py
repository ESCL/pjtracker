__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....resources.factories import EmployeeFactory, EquipmentFactory
from ....work.factories import ProjectFactory, ActivityFactory, ActivityGroupFactory, ActivityGroupTypeFactory
from ....work.models import Project


class Command(BaseCommand):
    """
    Create a project with a full activity WBS and a team with two employees
    and one excavator.

    This can be used to populate the database after a migration.

    :return: created project
    """
    def handle(self, **options):
        if Project.objects.exists():
            print('Project {} already exists, nothing to do.'.format(Project.objects.all()[0]))
            return

        # Setup activity groups
        print('Setting up activity groups...')
        ph = ActivityGroupTypeFactory.create(name='Phase')
        ds = ActivityGroupTypeFactory.create(name='Discipline')
        ph_eng = ActivityGroupFactory.create(name='Engineering', code='ENG', type=ph)
        ph_prt = ActivityGroupFactory.create(name='Procurement', code='PRT', type=ph)
        ph_cst = ActivityGroupFactory.create(name='Construction', code='CST', type=ph)
        ds_civ = ActivityGroupFactory.create(name='Civil', code='CIV', type=ds)
        ds_str = ActivityGroupFactory.create(name='Structural', code='STR', type=ds)
        ds_mec = ActivityGroupFactory.create(name='Mechanical', code='MEC', type=ds)
        print('Created activity groups: {}'.format([ph_eng, ph_prt, ph_cst, ds_civ, ds_str, ds_mec]))

        # Create project and activities
        print('Creating project...')
        proj = ProjectFactory.create(name='Some plant revamping')
        ac_cmp = ActivityFactory.create(code='CMP', name='Temporary Camp', project=proj)
        ActivityFactory.create(code='DES', name='Engineering', project=proj, parent=ac_cmp,
                               groups=[ph_eng, ds_civ], managerial_labour=True)
        ActivityFactory.create(code='PRT', name='Procurement', project=proj, parent=ac_cmp,
                               groups=[ph_prt, ds_civ], managerial_labour=True)
        ActivityFactory.create(code='CST', name='Construction', project=proj, parent=ac_cmp,
                               groups=[ph_cst, ds_civ], indirect_labour=True, direct_labour=True)
        ac_tr1 = ActivityFactory.create(code='TR1', name='Train 1', project=proj)
        u1 = ActivityFactory.create(code='U1', name='Unit 1', project=proj, parent=ac_tr1)
        u1_fnd = ActivityFactory.create(code='FNS', name='Foundations', project=proj, parent=u1)
        ActivityFactory.create(code='DES', name='Unit 1 Foundation Design', project=proj, parent=u1_fnd,
                               groups=[ph_eng, ds_civ], managerial_labour=True)
        ActivityFactory.create(code='SUP', name='Unit 1 Concrete Supply', project=proj, parent=u1_fnd,
                               groups=[ph_prt, ds_civ])
        ActivityFactory.create(code='CST', name='Unit 1 Foundation Construction', project=proj, parent=u1_fnd,
                               groups=[ph_cst, ds_civ])
        u1_eq = ActivityFactory.create(code='EQP', name='Unit 1 HP Drum', project=proj, parent=u1)
        ActivityFactory.create(code='DES', name='Unit 1 HP Drum Design', project=proj, parent=u1_eq,
                               groups=[ph_eng, ds_mec], managerial_labour=True)
        ActivityFactory.create(code='SUP', name='Unit 1 HP Drum Supply', project=proj, parent=u1_eq,
                               groups=[ph_prt, ds_mec])
        ActivityFactory.create(code='INS', name='Unit 1 HP Drum Installation', project=proj, parent=u1_eq,
                               groups=[ph_cst, ds_mec])
        u1_str = ActivityFactory.create(code='STR', name='Unit 1 Structure', project=proj, parent=u1)
        ActivityFactory.create(code='DES', name='Unit 1 Structure Design', project=proj, parent=u1_str,
                               groups=[ph_eng, ds_str], managerial_labour=True)
        ActivityFactory.create(code='SUP', name='Unit 1 Structure Supply', project=proj, parent=u1_str,
                               groups=[ph_prt, ds_str])
        ActivityFactory.create(code='CST', name='Unit 1 Structure Erection', project=proj, parent=u1_str,
                               groups=[ph_cst, ds_str])
        u1_pip = ActivityFactory.create(code='PIP', name='Unit 1 Piping', project=proj, parent=u1)
        ActivityFactory.create(code='DES', name='Unit 1 Piping Design', project=proj, parent=u1_pip,
                               groups=[ph_eng, ds_mec])
        ActivityFactory.create(code='SUP', name='Unit 1 Piping Supply', project=proj, parent=u1_pip,
                               groups=[ph_prt, ds_mec])
        ActivityFactory.create(code='CST', name='Unit 1 Piping Installation', project=proj, parent=u1_pip,
                               groups=[ph_cst, ds_mec])
        print('Created project "{}" with activities {}'.format(proj, proj.activity_set.all()))

        # Create one team with two employees and one machine
        print('Creating teams...')
        em1 = EmployeeFactory.create(project=proj)
        EmployeeFactory.create(project=proj, company=em1.company, team=em1.team)
        EquipmentFactory.create(project=proj, company=em1.company, team=em1.team)
        print('Created team "{}" with resources {}'.format(em1.team, em1.team.resource_set.all()))

        # Return the project
        print('Done.'.format(proj))
