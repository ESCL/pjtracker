__author__ = 'kako'

from django.conf.urls import url

from .views.apps import HomeView as AppHomeView
from .views.public import PublicView


urlpatterns = [
    url(r'^$', PublicView.as_view(), {'page': 'home'}, name='public'),
    url(r'^home$', AppHomeView.as_view(), name='home-app'),
    url(r'^(?P<page>\w+)$', PublicView.as_view(), name='public'),
]
