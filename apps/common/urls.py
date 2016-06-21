__author__ = 'kako'

from django.conf.urls import url
from oauth2_provider.views.base import TokenView, RevokeTokenView

from .views.apps import HomeView as AppHomeView
from .views.oauth import CustomAuthorizationView
from .views.public import PublicView


app_home_view = AppHomeView.as_view()
public_view = PublicView.as_view()
oauth_auth_view = CustomAuthorizationView.as_view()
oauth_token_view = TokenView.as_view()
oauth_revoke_view = RevokeTokenView.as_view()

urlpatterns = [
    url(r'^$', app_home_view, name='home'),
    url(r'^(?P<page>\w+)$', public_view, name='public'),

    url(r'^oauth/authorize/$', oauth_auth_view, name="authorize"),
    url(r'^oauth/token/$', oauth_token_view, name="token"),
    url(r'^oauth/revoke_token/$', oauth_revoke_view, name="revoke-token"),
]
