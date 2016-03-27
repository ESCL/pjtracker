__author__ = 'kako'

from django.core.exceptions import ValidationError
from factory import DjangoModelFactory, Faker, SubFactory, post_generation, LazyAttribute, SelfAttribute

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

    project = SubFactory(ProjectBaseFactory, owner=SelfAttribute('..owner'))
    owner = SubFactory(AccountBaseFactory)

    @classmethod
    def create(cls, **kwargs):
        """
        Process params with wbs_code before creating the object.
        """
        full_wbs_code = kwargs.pop('full_wbs_code', None)
        if full_wbs_code:
            cls._get_model_class().process_wbs_code_kwargs(full_wbs_code, kwargs)
        return super(ActivityBaseFactory, cls).create(**kwargs)


# Smart factories
# These produce fake data, used in unit tests and to bootstrap dev dbs

class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('street_address')
    code = Faker('military_ship')


class ActivityFactory(DjangoModelFactory):

    class Meta:
        model = Activity

    owner = LazyAttribute(lambda obj: obj.project.owner)
    name = 'Foundation 23 Design'
    code = 'FND23'
    project = SubFactory(ProjectFactory)

    @classmethod
    def create(cls, **kwargs):
        """
        Assign project kwarg if a parent was supplied before creating instance.
        """
        parent = kwargs.get('parent')
        project = kwargs.get('project')
        if parent and not project:
            kwargs['project'] = parent.project
        return super(ActivityFactory, cls).create(**kwargs)

    @post_generation
    def groups(self, create, values):
        if create and values:
            self.groups.add(*values)

    @post_generation
    def labour_types(self, create, values):
        if create and values:
            self.labour_types.add(*values)
