__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, post_generation

from .models import Project, Activity, ActivityGroup, ActivityGroupType


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

    name = 'Foundation 23 Design'
    code = 'FND23'
    project = SubFactory(ProjectFactory)

    @post_generation
    def groups(self, create, groups, **kwargs):
        if create and groups:
            self.groups.add(*groups)
