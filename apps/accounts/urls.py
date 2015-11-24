__author__ = 'kako'

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import SettingsView, UserView


urlpatterns = [
    # Auth views
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),

    # Settings view
    url(r'^settings/$', SettingsView.as_view(), name='settings'),

    # Users view
    url(r'^users/$', UserView.as_view(), name='users'),
    url(r'^users/(?P<pk>\d+)/$', UserView.as_view(), name='user'),
    url(r'^users/(?P<pk>\d+)/(?P<action>edit)/$', UserView.as_view(), name='user'),
]
