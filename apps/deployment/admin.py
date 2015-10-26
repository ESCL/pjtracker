from django.contrib import admin

from .models import TimeSheet, WorkLog


class WorkLogInline(admin.TabularInline):
    model = WorkLog
    exclude = ('company', 'position', 'location',)


class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('team', 'date', 'status', 'issuer', 'timestamp',)
    inlines = (WorkLogInline,)


admin.site.register(TimeSheet, TimeSheetAdmin)
