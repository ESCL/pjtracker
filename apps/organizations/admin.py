from django.contrib import admin

from .models import Company, Department, Team, Position, PositionLabourType


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner',)


class PositionLabourTypeAdmin(admin.ModelAdmin):
    list_display = ('position', 'labour_type', 'owner',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'company', 'owner',)
    filter_horizontal = ('activities',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PositionLabourType, PositionLabourTypeAdmin)
admin.site.register(Team, TeamAdmin)
