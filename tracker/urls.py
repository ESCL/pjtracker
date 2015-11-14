from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Common app, with public and main app views
    url(r'^', include('apps.common.urls')),

    # Specific app views (modules)
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^geo/', include('apps.geo.urls')),
    url(r'^organizations/', include('apps.organizations.urls')),
    url(r'^resources/', include('apps.resources.urls')),
    url(r'^work/', include('apps.work.urls')),
    url(r'^deployment/', include('apps.deployment.urls')),
    url(r'^notifications/', include('apps.notifications.urls')),

    # Admin dashboard
    url(r'^admin/', include(admin.site.urls)),
]
