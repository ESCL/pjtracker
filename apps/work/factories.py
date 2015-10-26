__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, post_generation

from ..geo.factories import LocationFactory
from .models import Project, Activity, ActivityGroup, ActivityGroupType


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('street_address')
    code = Faker('military_ship')
    location = SubFactory(LocationFactory)


class ActivityGroupTypeFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroupType

    name = 'Phase'


class ActivityGroupFactory(DjangoModelFactory):

    class Meta:
        model = ActivityGroup

    name = 'Engineering'
    code = 'ENG'
    type = SubFactory(ActivityGroupTypeFactory)


class ActivityFactory(DjangoModelFactory):

    class Meta:
        model = Activity

    name = 'Foundation 23 Design'
    code = 'FND23'
    project = SubFactory(ProjectFactory)

    @post_generation
    def groups(self, create, groups, **kwargs):
        if create and groups:
            self.groups.add(*groups)


def create_full_project():
    """
    Crete a project with a full activity WBS.
    :return: created project
    """
    ph = ActivityGroupTypeFactory.create(name='Phase')
    ds = ActivityGroupTypeFactory.create(name='Discipline')

    # Create project and main groups for activities
    proj = ProjectFactory.create(name='Some plant revamping')
    ph_eng = ActivityGroupFactory.create(name='Engineering', code='ENG', type=ph)
    ph_prt = ActivityGroupFactory.create(name='Procurement', code='PRT', type=ph)
    ph_cst = ActivityGroupFactory.create(name='Construction', code='CST', type=ph)
    ds_civ = ActivityGroupFactory.create(name='Civil', code='CIV', type=ds)
    ds_str = ActivityGroupFactory.create(name='Structural', code='STR', type=ds)
    ds_mec = ActivityGroupFactory.create(name='Mechanical', code='MEC', type=ds)

    # Create camp wbs
    ac_cmp = ActivityFactory.create(code='CMP', name='Temporary Camp', project=proj)
    ActivityFactory.create(code='DES', name='Engineering', project=proj, parent=ac_cmp, groups=[ph_eng, ds_civ])
    ActivityFactory.create(code='PRT', name='Procurement', project=proj, parent=ac_cmp, groups=[ph_prt, ds_civ])
    ActivityFactory.create(code='CST', name='Construction', project=proj, parent=ac_cmp, groups=[ph_cst, ds_civ])

    # Create train 1 wbs
    ac_tr1 = ActivityFactory.create(code='TR1', name='Train 1', project=proj)
    u1 = ActivityFactory.create(code='U1', name='Unit 1', project=proj, parent=ac_tr1)
    u1_fnd = ActivityFactory.create(code='FNS', name='Foundations', project=proj, parent=u1)
    ActivityFactory.create(code='DES', name='Unit 1 Foundation Design', project=proj, parent=u1_fnd, groups=[ph_eng, ds_civ])
    ActivityFactory.create(code='SUP', name='Unit 1 Concrete Supply', project=proj, parent=u1_fnd, groups=[ph_prt, ds_civ])
    ActivityFactory.create(code='CST', name='Unit 1 Foundation Construction', project=proj, parent=u1_fnd, groups=[ph_cst, ds_civ])
    u1_eq = ActivityFactory.create(code='EQP', name='Unit 1 HP Drum', project=proj, parent=u1)
    ActivityFactory.create(code='DES', name='Unit 1 HP Drum Design', project=proj, parent=u1_eq, groups=[ph_eng, ds_mec])
    ActivityFactory.create(code='SUP', name='Unit 1 HP Drum Supply', project=proj, parent=u1_eq, groups=[ph_prt, ds_mec])
    ActivityFactory.create(code='INS', name='Unit 1 HP Drum Installation', project=proj, parent=u1_eq, groups=[ph_cst, ds_mec])
    u1_str = ActivityFactory.create(code='STR', name='Unit 1 Structure', project=proj, parent=u1)
    ActivityFactory.create(code='DES', name='Unit 1 Structure Design', project=proj, parent=u1_str, groups=[ph_eng, ds_str])
    ActivityFactory.create(code='SUP', name='Unit 1 Structure Supply', project=proj, parent=u1_str, groups=[ph_prt, ds_str])
    ActivityFactory.create(code='CST', name='Unit 1 Structure Erection', project=proj, parent=u1_str, groups=[ph_cst, ds_str])
    u1_pip = ActivityFactory.create(code='PIP', name='Unit 1 Piping', project=proj, parent=u1)
    ActivityFactory.create(code='DES', name='Unit 1 Piping Design', project=proj, parent=u1_pip, groups=[ph_eng, ds_mec])
    ActivityFactory.create(code='SUP', name='Unit 1 Piping Supply', project=proj, parent=u1_pip, groups=[ph_prt, ds_mec])
    ActivityFactory.create(code='CST', name='Unit 1 Piping Installation', project=proj, parent=u1_pip, groups=[ph_cst, ds_mec])

    # Return project
    return proj
