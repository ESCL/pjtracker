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
