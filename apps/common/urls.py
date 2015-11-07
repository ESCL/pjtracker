__author__ = 'kako'

from django.conf.urls import url

from .views.apps import HomeView as AppHomeView
from .views.public import PublicView


urlpatterns = [
    url(r'^$', AppHomeView.as_view(), name='home'),
    url(r'^(?P<page>\w+)$', PublicView.as_view(), name='public'),
]
