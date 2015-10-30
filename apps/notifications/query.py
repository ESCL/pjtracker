__author__ = 'kako'

from django.db.models.query import QuerySet


class NotificationQuerySet(QuerySet):

    def for_user(self, user):
        if user.is_authenticated:
            return self.filter(recipient=user.id)
        return self
