from django.contrib import admin

from .models import Company, Team


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'company', 'owner',)
    filter_horizontal = ('activities',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Team, TeamAdmin)
