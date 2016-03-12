from django.contrib import admin

from .models import TimeSheet, TimeSheetAction, TimeSheetSettings, WorkLog


class WorkLogInline(admin.TabularInline):
    model = WorkLog
    exclude = ('owner', 'company', 'position', 'location',)


class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('owner', 'team', 'date', 'status',)
    inlines = (WorkLogInline,)


class TimeSheetActionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'timesheet', 'actor', 'action', 'timestamp',)


class TimeSheetSettingsAdmin(admin.ModelAdmin):
    list_display = ('account', 'approval_policy', 'rejection_policy',)


admin.site.register(TimeSheet, TimeSheetAdmin)
admin.site.register(TimeSheetAction, TimeSheetActionAdmin)
admin.site.register(TimeSheetSettings, TimeSheetSettingsAdmin)
