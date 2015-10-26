from django.contrib import admin

from .models import Project, Activity, ActivityGroup, ActivityGroupType


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'location',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'project', 'parent',)


class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)


class ActivityGroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityGroup, ActivityGroupAdmin)
admin.site.register(ActivityGroupType, ActivityGroupTypeAdmin)
