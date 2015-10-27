__author__ = 'kako'

from django.db.models.query import QuerySet

from ..exceptions import AuthenticationError


class OwnedEntityQuerySet(QuerySet):
    """
    Restrict the queryset to objects that belong to the user account's domain,
    which means that they either belong to the account or are global (have no
    owner).

    This override also covers get(), since it calls this method first.
    """
    def filter(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
            account = user.profile.account

        except KeyError:
            raise AuthenticationError('OwnedEntity filters require an authenticated user.')

        except AttributeError:
            raise AuthenticationError('OwnedEntity filters require a user with an account.')

        else:
            kwargs['owner__in'] = (account, None)
            return super(OwnedEntityQuerySet, self).filter(*args, **kwargs)

