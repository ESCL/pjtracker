__author__ = 'kako'

from django.conf.urls import url, include
from tastypie.api import Api

from .api.resources import NotificationsResource


api_v0 = Api(api_name='v0')
api_v0.register(NotificationsResource())

urlpatterns = [
    # APIs
    url('^api/', include(api_v0.urls))
]
