from django.contrib import admin

from .models import Company, Team, Position, PositionLabourType


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name',)


class PositionLabourTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'position', 'labour_type',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name', 'company',)
    filter_horizontal = ('activities',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PositionLabourType, PositionLabourTypeAdmin)
admin.site.register(Team, TeamAdmin)
