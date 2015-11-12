__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, post_generation, LazyAttribute

from .models import Project, Activity, ActivityGroup, ActivityGroupType, LabourType


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('street_address')
    code = Faker('military_ship')


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

    owner = LazyAttribute(lambda obj: obj.project.owner)
    name = 'Foundation 23 Design'
    code = 'FND23'
    project = SubFactory(ProjectFactory)

    @post_generation
    def groups(self, create, values):
        if create and values:
            self.groups.add(*values)

    @post_generation
    def labour_types(self, create, values):
        if create and values:
            self.labour_types.add(*values)


class IndirectLabourFactory(DjangoModelFactory):

    class Meta:
        model = LabourType

    name = 'Indirect Labour'
    code = 'IN'


class DirectLabourFactory(DjangoModelFactory):

    class Meta:
        model = LabourType

    name = 'Direct Labour'
    code = 'DI'
