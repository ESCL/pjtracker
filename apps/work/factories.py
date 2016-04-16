__author__ = 'kako'

from factory import DjangoModelFactory, Faker, SubFactory, post_generation, LazyAttribute, SelfAttribute

from ..accounts.factories import AccountBaseFactory
from .models import Project, Activity, LabourType


# Base factories
# These generate no fake data, they are used for imports and as base classes

class ProjectBaseFactory(DjangoModelFactory):

    class Meta:
        model = Project
        django_get_or_create = ('owner', 'code',)

    owner = SubFactory(AccountBaseFactory)


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


class LabourTypeFactory(DjangoModelFactory):

    class Meta:
        model = LabourType
        django_get_or_create = ('owner', 'code',)


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
    code = 'FND2'
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
