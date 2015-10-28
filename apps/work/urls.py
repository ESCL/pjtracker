__author__ = 'kako'

from django.conf.urls import url

from .views import ProjectView


urlpatterns = [
    url(r'^projects/$', ProjectView.as_view(), name='projects'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectView.as_view(), name='project')
]
