__author__ = 'kako'

from django.core.exceptions import ValidationError
from factory import DjangoModelFactory, Faker, SubFactory, post_generation, LazyAttribute, PostGeneration

from ..accounts.factories import AccountBaseFactory
from .models import Project, Activity, ActivityGroup, ActivityGroupType, LabourType


# Base factories
# These generate no fake data, they are used for imports and as base classes

class ProjectBaseFactory(DjangoModelFactory):

    class Meta:
        model = Project
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountBaseFactory)


def set_subfactory_project(container, create, project, **kwargs):
    """
    Set the correct project for the container factory, which could be passed
    directly (project) or need to be created (from kwargs).
    """
    if project:
        # We got a project instance already, set it
        container.project = project

    elif kwargs:
        # We got some attrs for project, let's build/create it
        method_name = create and 'create' or 'build'
        method = getattr(ProjectBaseFactory, method_name)
        if 'code' not in kwargs:
            import pdb; pdb.set_trace()
        try:
            container.project = method(owner=container.owner, **kwargs)
            container.project.full_clean()

        except KeyError as e:
            errors = {a: 'This field is required' for a in e.args}
            raise ValidationError(errors)


class ActivityBaseFactory(DjangoModelFactory):

    class Meta:
        model = Activity
        django_get_or_create = ('owner', 'parent', 'code',)

    owner = SubFactory(AccountBaseFactory)
    project = PostGeneration(lambda obj, create, project, **kwargs: set_subfactory_project)


# Helper functions


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class ProjectFactory(ProjectBaseFactory):

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


class ActivityFactory(ActivityBaseFactory):

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


class ManagementLabourFactory(DjangoModelFactory):

    class Meta:
        model = LabourType

    name = 'Management'
    code = 'MG'


class IndirectLabourFactory(DjangoModelFactory):

    class Meta:
        model = LabourType

    name = 'Indirect'
    code = 'IN'


class DirectLabourFactory(DjangoModelFactory):

    class Meta:
        model = LabourType

    name = 'Direct'
    code = 'DI'
