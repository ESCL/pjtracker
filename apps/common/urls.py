__author__ = 'kako'

from django.conf.urls import url
from oauth2_provider.views.base import TokenView, RevokeTokenView

from .views.apps import HomeView as AppHomeView
from .views.oauth import CustomAuthorizationView
from .views.public import PublicView


urlpatterns = [
    url(r'^$', AppHomeView.as_view(), name='home'),
    url(r'^(?P<page>\w+)$', PublicView.as_view(), name='public'),

    url(r'^oauth/authorize/$', CustomAuthorizationView.as_view(), name="authorize"),
    url(r'^oauth/token/$', TokenView.as_view(), name="token"),
    url(r'^oauth/revoke_token/$', RevokeTokenView.as_view(), name="revoke-token"),
]
