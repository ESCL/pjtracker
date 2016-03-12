from django.contrib import admin

from .models import Project, Activity, ActivityGroup, ActivityGroupType, LabourType


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('owner', 'wbs_code', 'name', 'project',)


class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ('owner', 'type', 'code', 'name',)


class ActivityGroupTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name',)


class LabourTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityGroup, ActivityGroupAdmin)
admin.site.register(ActivityGroupType, ActivityGroupTypeAdmin)
admin.site.register(LabourType, LabourTypeAdmin)
