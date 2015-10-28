__author__ = 'kako'

from django.conf.urls import url

from .views.apps import HomeView as AppHomeView


urlpatterns = [
    url(r'^$', AppHomeView.as_view(), name='app-home'),
]
