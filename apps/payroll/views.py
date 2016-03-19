__author__ = 'kako'

from django.shortcuts import render, redirect

from ..common.views.base import SafeView, StandardResourceView
from .models import CalendarDay, HourType, Period, WorkedHours
from .forms import (CalendarDayForm, CalendarDaySearchForm,
                    HourTypeForm, HourTypeSearchForm,
                    PeriodForm, PeriodSearchForm, WorkedHoursForm)


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


class WorkedHoursView(SafeView):
    process_form = WorkedHoursForm
    list_template = 'worked-hours.html'
    process_template = 'worked-hours-process.html'

    @classmethod
    def authorize(cls, request, action):
        return

    def get(self, request, period_pk, action=None):
        # Get period and build context
        period = Period.objects.get(id=period_pk)
        ctx = {'period': period}

        # Select template and update context based on action
        if action == 'process':
            ctx['form'] = self.process_form()
            template = self.process_template
        else:
            # TODO: add filter form
            # Determine phases to show
            # Note: real vs. payroll hours
            mode = request.GET.get('mode')
            if mode == 'real':
                phases = [WorkedHours.PHASE_ACTUAL, WorkedHours.PHASE_RETROACTIVE]
            else:
                phases = [WorkedHours.PHASE_ADJUSTMENT, WorkedHours.PHASE_ACTUAL, WorkedHours.PHASE_FORECAST]

            ctx['worked_hours'] = WorkedHours.objects.filter(period=period, phase__in=phases)
            template = self.list_template

        # Render template
        return render(request, template, ctx)

    def post(self, request, period_pk, action):
        # Get period and init form
        period = Period.objects.get(id=period_pk)
        form = self.process_form(request.POST)

        # Validate form
        if form.is_valid():
            # Valid, process and save and redirect to collection view
            WorkedHours.clear_for_period(period)
            worked_hours = WorkedHours.calculate_for_period(period)
            for wh in worked_hours:
                wh.save()
            return redirect('worked-hours', period_pk=period_pk)

        else:
            # Invalid form, re-render form with errors
            ctx = {'period': period, 'form': form}
            return render(request, self.process_template, ctx, status=400)
