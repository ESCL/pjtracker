from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Common app, with public and main app views
    url(r'^', include('apps.common.urls')),

    # Specific app views (modules)
    url(r'^account/', include('apps.accounts.urls')),
    url(r'^notifications/', include('apps.notifications.urls')),
    url(r'^organizations/', include('apps.organizations.urls')),
    url(r'^resources/', include('apps.resources.urls')),
    url(r'^wbs/', include('apps.work.urls')),
    url(r'^work/', include('apps.deployment.urls')),
    url(r'^payroll/', include('apps.payroll.urls')),

    # OAuth2 provider
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Admin dashboard
    url(r'^admin/', include(admin.site.urls)),
]
