__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....accounts.factories import Account
from ...factories import ProjectFakeFactory, ActivityFakeFactory
from ...models import LabourType, ActivityGroup


class Command(BaseCommand):
    """
    Create a project with a full activity WBS and a team with two employees
    and one excavator.

    This can be used to populate the database after a migration.

    :return: created project
    """
    def handle(self, **options):
        self.stdout.write('Creating project...')
        account = Account.objects.get()
        mgt = LabourType.objects.get(code='MG')
        ind = LabourType.objects.get(code='IN')
        dir = LabourType.objects.get(code='DI')

        # First get default activity groups
        ph_eng = ActivityGroup.objects.get(name='Engineering')
        ph_prt = ActivityGroup.objects.get(name='Procurement')
        ph_cst = ActivityGroup.objects.get(name='Construction')
        ds_civ = ActivityGroup.objects.get(name='Civil')
        ds_str = ActivityGroup.objects.get(name='Structural')
        ds_mec = ActivityGroup.objects.get(name='Mechanical')
        ds_pip = ActivityGroup.objects.get(name='Piping')

        # Create the project
        proj = ProjectFakeFactory.create(owner=account, name='Some plant revamping')

        # Create temp camp activities
        ac_cmp = ActivityFakeFactory.create(code='CMP', name='Temporary Camp', project=proj)
        ActivityFakeFactory.create(code='DES', name='Engineering', project=proj, parent=ac_cmp,
                               groups=[ph_eng, ds_civ], labour_types=[mgt])
        ActivityFakeFactory.create(code='PRT', name='Procurement', project=proj, parent=ac_cmp,
                               groups=[ph_prt, ds_civ], labour_types=[mgt, ind])
        ActivityFakeFactory.create(code='CST', name='Construction', project=proj, parent=ac_cmp,
                               groups=[ph_cst, ds_civ], labour_types=[ind, dir])

        # Create train 1 main activity
        ac_tr1 = ActivityFakeFactory.create(code='TR1', name='Train 1', project=proj)

        # Create train 1 civil works activities
        u1 = ActivityFakeFactory.create(code='U1', name='Unit 1', project=proj, parent=ac_tr1)
        u1_fnd = ActivityFakeFactory.create(code='FND', name='Foundations', project=proj, parent=u1)
        ActivityFakeFactory.create(code='DES', name='Unit 1 Foundation Design', project=proj, parent=u1_fnd,
                               groups=[ph_eng, ds_civ], labour_types=[mgt])
        ActivityFakeFactory.create(code='SUP', name='Unit 1 Concrete Supply', project=proj, parent=u1_fnd,
                               groups=[ph_prt, ds_civ], labour_types=[mgt, ind])
        ActivityFakeFactory.create(code='CST', name='Unit 1 Foundation Construction', project=proj, parent=u1_fnd,
                               groups=[ph_cst, ds_civ], labour_types=[ind, dir])

        # Create train 1 structural activities
        u1_str = ActivityFakeFactory.create(code='STR', name='Unit 1 Structure', project=proj, parent=u1)
        ActivityFakeFactory.create(code='DES', name='Unit 1 Structure Design', project=proj, parent=u1_str,
                               groups=[ph_eng, ds_str], labour_types=[mgt])
        ActivityFakeFactory.create(code='SUP', name='Unit 1 Structure Supply', project=proj, parent=u1_str,
                               groups=[ph_prt, ds_str])
        ActivityFakeFactory.create(code='CST', name='Unit 1 Structure Erection', project=proj, parent=u1_str,
                               groups=[ph_cst, ds_str])

        # Create train 1 mechanical activities
        u1_eq = ActivityFakeFactory.create(code='EQP', name='Unit 1 HP Drum', project=proj, parent=u1)
        ActivityFakeFactory.create(code='DES', name='Unit 1 HP Drum Design', project=proj, parent=u1_eq,
                               groups=[ph_eng, ds_mec], labour_types=[mgt])
        ActivityFakeFactory.create(code='SUP', name='Unit 1 HP Drum Supply', project=proj, parent=u1_eq,
                               groups=[ph_prt, ds_mec])
        ActivityFakeFactory.create(code='INS', name='Unit 1 HP Drum Installation', project=proj, parent=u1_eq,
                               groups=[ph_cst, ds_mec])

        # Create train 1 piping activities
        u1_pip = ActivityFakeFactory.create(code='PIP', name='Unit 1 Piping', project=proj, parent=u1)
        ActivityFakeFactory.create(code='DES', name='Unit 1 Piping Design', project=proj, parent=u1_pip,
                               groups=[ph_eng, ds_mec])
        ActivityFakeFactory.create(code='SUP', name='Unit 1 Piping Supply', project=proj, parent=u1_pip,
                               groups=[ph_prt, ds_mec])
        ActivityFakeFactory.create(code='CST', name='Unit 1 Piping Installation', project=proj, parent=u1_pip,
                               groups=[ph_cst, ds_pip])

        # Done, print result
        self.stdout.write('Created project "{}" with activities {}.'.format(proj, proj.activity_set.all()))
