__author__ = 'kako'

from django.conf.urls import url

from .views.apps import HomeView as AppHomeView
from .views.public import HomeView as PublicHomeView


urlpatterns = [
    url(r'^$', PublicHomeView.as_view(), name='public-home'),
    url(r'^main$', AppHomeView.as_view(), name='app-home'),
]
