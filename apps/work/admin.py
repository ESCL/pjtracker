from django.contrib import admin

from .models import (
    Project, Inactivity, Activity, ActivityGroup, ActivityGroupType, LabourType
)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('wbs_code', 'name', 'project', 'owner',)


class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ('type', 'code', 'name', 'owner',)


class ActivityGroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)


class InactivityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'owner')


class LabourTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'owner',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityGroup, ActivityGroupAdmin)
admin.site.register(ActivityGroupType, ActivityGroupTypeAdmin)
admin.site.register(Inactivity, InactivityAdmin)
admin.site.register(LabourType, LabourTypeAdmin)
