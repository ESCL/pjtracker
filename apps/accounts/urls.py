__author__ = 'kako'

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import SettingsView, UserView


settings_view = SettingsView.as_view()
user_view = UserView.as_view()

urlpatterns = [
    # Auth views
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^password/$', auth_views.password_change,
        {'template_name': 'password-change.html'}, name='password_change'),
    url(r'^password/changed/$', auth_views.password_change_done,
        {'template_name': 'password-changed.html'}, name='password_change_done'),

    # Settings view
    url(r'^settings/$', settings_view, name='settings'),

    # Users view
    url(r'^users/$', user_view, name='users'),
    url(r'^users/(?P<pk>\d+)/$', user_view, name='user'),
    url(r'^users/(?P<pk>\d+)/(?P<action>edit)/$', user_view, name='user'),
]
