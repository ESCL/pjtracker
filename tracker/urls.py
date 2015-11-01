from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Common app, with public and main app views
    url(r'^', include('apps.common.urls')),

    # Specific app views (modules)
    url(r'^', include('apps.accounts.urls')),
    url(r'^', include('apps.geo.urls')),
    url(r'^', include('apps.organizations.urls')),
    url(r'^', include('apps.resources.urls')),
    url(r'^', include('apps.work.urls')),
    url(r'^', include('apps.deployment.urls')),

    # Admin dashboard
    url(r'^admin/', include(admin.site.urls)),
]
