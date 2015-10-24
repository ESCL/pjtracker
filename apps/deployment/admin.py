from django.contrib import admin

from .models import TimeSheet, WorkLog


class WorkLogInline(admin.TabularInline):
    model = WorkLog


class TimeSheetAdmin(admin.ModelAdmin):
    inlines = (WorkLogInline,)


admin.site.register(TimeSheet, TimeSheetAdmin)
