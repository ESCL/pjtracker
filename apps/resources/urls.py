__author__ = 'kako'

from django.conf.urls import include, url
from django.contrib import admin

from .views import EmployeeView


urlpatterns = [
    # Examples:
    # url(r'^$', 'tracker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^employees/', EmployeeView.as_view()),
]
