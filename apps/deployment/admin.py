from django.contrib import admin

from .models import (
    Presence, TimeSheet, TimeSheetAction, TimeSheetSettings, WorkLog
)


class WorkLogInline(admin.TabularInline):
    model = WorkLog
    exclude = ('owner',)


class PresenceAdmin(admin.ModelAdmin):
    list_display = ('timesheet', 'resource', 'owner')
    inlines = (WorkLogInline,)


class PresenceInline(admin.TabularInline):
    model = Presence
    exclude = ('owner', 'company', 'location', 'department', 'position',
               'category', 'equipment_type',)


class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('team', 'date', 'status', 'owner',)
    inlines = (PresenceInline,)


class TimeSheetActionAdmin(admin.ModelAdmin):
    list_display = ('timesheet', 'actor', 'action', 'timestamp', 'owner',)


class TimeSheetSettingsAdmin(admin.ModelAdmin):
    list_display = ('account', 'approval_policy', 'rejection_policy',)


admin.site.register(Presence, PresenceAdmin)
admin.site.register(TimeSheet, TimeSheetAdmin)
admin.site.register(TimeSheetAction, TimeSheetActionAdmin)
admin.site.register(TimeSheetSettings, TimeSheetSettingsAdmin)
