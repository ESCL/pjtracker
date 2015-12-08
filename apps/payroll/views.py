__author__ = 'kako'

from ..common.views.base import StandardResourceView

from .models import CalendarDay, HourType, Period
from .forms import (CalendarDayForm, CalendarDaySearchForm,
                    HourTypeForm, HourTypeSearchForm,
                    PeriodForm, PeriodSearchForm)


class CalendarDayView(StandardResourceView):
    model = CalendarDay
    main_form = CalendarDayForm
    search_form = CalendarDaySearchForm
    list_template = 'calendar.html'
    detail_template = 'calendar-day.html'
    edit_template = 'calendar-day-edit.html'
    collection_view_name = 'calendar'


class HourTypeView(StandardResourceView):
    model = HourType
    main_form = HourTypeForm
    search_form = HourTypeSearchForm
    list_template = 'hour-types.html'
    detail_template = 'hour-type.html'
    edit_template = 'hour-type-edit.html'
    collection_view_name = 'hour-types'


class PeriodView(StandardResourceView):
    model = Period
    main_form = PeriodForm
    search_form = PeriodSearchForm
    list_template = 'periods.html'
    detail_template = 'period.html'
    edit_template = 'period-edit.html'
