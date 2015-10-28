__author__ = 'kako'

from django.db.models.query import QuerySet

from ..exceptions import AuthenticationError


class OwnedEntityQuerySet(QuerySet):
    """
    Restrict the queryset to objects that belong to the user account's domain
    for users that are not staff, so they can only see objects that are owned by
    their account.

    Note: since this is a queryset method, managers must use it after filter,
    so for using it with get(), we need to pass the params to filter and then
    use get() without parameters, like:
        obj = model.objects.filter(pk=pk).for_user(user).get()
    """
    def for_user(self, user):
        if user.is_staff or user.is_superuser:
            return self

        try:
            account = user.profile.account

        except AttributeError:
            raise AuthenticationError('OwnedEntity filters require a user with an account.')

        else:
            return self.filter(owner__in=(None, account))

