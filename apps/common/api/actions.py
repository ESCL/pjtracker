__author__ = 'kako'

from tastypie import resources, fields


class Action(object):

    def __init__(self, method_name=None, args=None, kwargs=None):
        self.name = method_name
        self.args = args or []
        self.kwargs = kwargs or {}

    def execute_for(self, instance):
        method = getattr(instance, self.name)
        return method(*self.args, **self.kwargs)


class ActionsResource(resources.Resource):

    actions = []
    instance_model = None

    class Meta:
        include_resource_uri = False
        object_class = Action
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = []

    name = fields.CharField(attribute='name')
    args = fields.ListField(attribute='args')
    kwargs = fields.DictField(attribute='kwargs')

    def _get_instance(self, **kwargs):
        pk = kwargs.get('pk')
        return self.instance_model.objects.get(pk=pk)

    def obj_get_list(self, bundle, **kwargs):
        return [Action(method_name) for method_name in self.actions]

    def obj_create(self, bundle, **kwargs):
        instance = self._get_instance(**kwargs)

        # Construct action and execute it
        bundle = self.full_hydrate(bundle)
        bundle.obj.execute_for(instance)
