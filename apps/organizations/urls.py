__author__ = 'kako'

from django.conf.urls import url

from .views import CompanyView, TeamView


urlpatterns = [
    # Companies view
    url(r'^companies/$', CompanyView.as_view(), name='companies'),

    # Teams view
    url(r'^teams/$', TeamView.as_view(), name='teams'),
]
