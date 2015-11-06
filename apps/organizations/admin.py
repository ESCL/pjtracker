from django.contrib import admin

from .models import Company, Team, Position


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'company', 'owner',)
    filter_horizontal = ('activities',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Team, TeamAdmin)
