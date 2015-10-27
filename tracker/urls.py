from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Common app, with public and main app views
    url(r'^', include('apps.common.urls')),

    # Specific app views (modules)
    url(r'^resources/', include('apps.resources.urls')),

    # Admin dashboard
    url(r'^admin/', include(admin.site.urls)),
]
