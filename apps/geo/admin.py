from django.contrib import admin

from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'owner',)


admin.site.register(Location, LocationAdmin)
