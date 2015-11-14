__author__ = 'kako'

from django.conf.urls import url
from tastypie import authorization, resources, utils

from ...common.api.actions import ActionsResource
from ..models import Notification


class NotificationActionsResource(ActionsResource):
    actions = ['dismiss']
    instance_model = Notification


class NotificationsResource(resources.ModelResource):

    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notifications'
        authorization = authorization.ReadOnlyAuthorization()

    def prepend_urls(self):
        regex = r'^(?P<resource_name>{})/(?P<pk>\w[\w/-]*)/actions{}$'.format(self._meta.resource_name,
                                                                            utils.trailing_slash())
        return [
            url(regex, self.wrap_view('dispatch_actions'), name='notification-actions'),
        ]

    def dispatch_actions(self, request, **kwargs):
        return NotificationActionsResource().dispatch('list', request, **kwargs)
