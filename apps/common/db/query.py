__author__ = 'kako'

from django.db.models.query import QuerySet, ValuesQuerySet

from ..exceptions import NotAuthenticatedError


class OwnedEntityQuerySet(QuerySet):
    """
    Restrict the queryset to objects that belong to the user account's domain
    for users that are not staff, so they can only see objects that are owned by
    their account. If include_global is True, it also includes objects without
    account.

    Note: since this is a queryset method, managers must use it after filter,
    so for using it with get(), we need to pass the params to filter and then
    use get() without parameters, like:
        obj = model.objects.filter(pk=pk).for_user(user).get()
    """
    include_global = True

    def for_user(self, user):
        qs = self
        try:
            account = user.domain
            if account:
                qs = self.filter(owner=account)
                if self.include_global:
                    qs = qs | self.filter(owner=None)

            return qs

        except AttributeError:
            raise NotAuthenticatedError('A user with account is required to view owned objects.')

    def for_owner(self, owner):
        return self.filter(owner=owner)


class ValuesGroup(object):
    """
    Generic object that constructs related objects like a Django model
    from queryset values() data. This is used as a workaround for Django's
    shitty behaviour of returning dicts instead of instances when using
    values() to group.
    """
    def __init__(self, model, values):
        self._model = model
        self._values = values
        self._build_data()
        self._populate_attrs()

    def _build_data(self):
        self._data = {}
        for k, v in self._values.items():
            attrs = k.split('__')
            first_attr = attrs[0]
            if len(attrs) > 1:
                if first_attr not in self._data:
                    self._data[first_attr] = {}
                for attr in attrs[1:]:
                    self._data[first_attr][attr] = v

            else:
                self._data[k] = v

    def _populate_attrs(self):
        for k, v in self._data.items():
            if isinstance(v, dict):
                try:
                    model = getattr(self._model, k).field.related.to
                    v = model(**v)
                except AttributeError:
                    continue
            setattr(self, k, v)


class ValuesGroupQuerySet(ValuesQuerySet):
    """
    Modified ValuesQuerySet that yields ValuesGroup instances instead
    of dictionaries, which means that you can still expect a model-like
    behaviour for APIs and whatnot. It just works.
    """
    def iterator(self):
        # Same as in django
        extra_names = list(self.query.extra_select)
        field_names = self.field_names
        annotation_names = list(self.query.annotation_select)
        names = extra_names + field_names + annotation_names

        # Iterate results and yield ValuesGroup instances
        for row in self.query.get_compiler(self.db).results_iter():
            data = dict(zip(names, row))
            obj = ValuesGroup(model=self.model, values=data)
            yield obj


class ValuesGroupMixin(QuerySet):
    """
    QuerySet mixin that uses ValuesGroupQuerySet as the values() queryset
    instead of the standard shitty one..
    """
    def values(self, *fields):
        return self._clone(klass=ValuesGroupQuerySet, setup=True, _fields=fields)

