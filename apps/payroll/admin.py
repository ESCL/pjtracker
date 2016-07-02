__author__ = 'kako'

from django.contrib import admin

from .models import CalendarDay, HourType, HourTypeRange, StandardHours, Period, WorkedHours


class CalendarDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'type', 'owner',)


class HourTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner',)


class HourTypeRangeAdmin(admin.ModelAdmin):
    list_display = ('day_type', 'limit', 'hour_type', 'owner',)


class StandardHoursAdmin(admin.ModelAdmin):
    list_display = ('day_type', 'hours', 'owner',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'start_date', 'end_date',
                    'forecast_start_date', 'owner',)
    exclude = ('code',)


class WorkedHoursAdmin(admin.ModelAdmin):
    list_display = ('period', 'phase', 'employee', 'hour_type', 'hours', 'owner',)


admin.site.register(CalendarDay, CalendarDayAdmin)
admin.site.register(HourType, HourTypeAdmin)
admin.site.register(HourTypeRange, HourTypeRangeAdmin)
admin.site.register(StandardHours, StandardHoursAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(WorkedHours, WorkedHoursAdmin)
