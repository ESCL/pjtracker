__author__ = 'kako'

from django.contrib import admin

from .models import CalendarDay, HourType, HourTypeRange, StandardHours, Period, WorkedHours


class CalendarDayAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'name', 'type',)


class HourTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'code',)


class HourTypeRangeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'day_type', 'limit', 'hour_type',)


class StandardHoursAdmin(admin.ModelAdmin):
    list_display = ('owner', 'day_type', 'hours',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'code', 'start_date', 'end_date',
                    'forecast_start_date',)
    exclude = ('code',)


class WorkedHoursAdmin(admin.ModelAdmin):
    list_display = ('owner', 'period', 'phase', 'employee', 'hour_type', 'hours',)


admin.site.register(CalendarDay, CalendarDayAdmin)
admin.site.register(HourType, HourTypeAdmin)
admin.site.register(HourTypeRange, HourTypeRangeAdmin)
admin.site.register(StandardHours, StandardHoursAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(WorkedHours, WorkedHoursAdmin)
