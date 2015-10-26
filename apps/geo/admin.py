from django.contrib import admin

from .models import Nation, Region, Locality, Location, Space


class NationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'nation',)


class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'locality', 'latitude', 'longitude',)


class SpaceAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'section', 'location',)


admin.site.register(Nation, NationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Space, SpaceAdmin)
