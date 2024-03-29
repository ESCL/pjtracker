__author__ = 'kako'

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.shortcuts import render, redirect

from ..common.utils import Indexable
from ..common.views.base import SafeView, StandardResourceView
from .models import CalendarDay, HourType, Period, WorkedHours
from .forms import (CalendarDayForm, CalendarDaySearchForm,
                    HourTypeForm, HourTypeSearchForm,
                    PeriodForm, PeriodSearchForm, ProcessPayrollForm)


class CalendarDayView(StandardResourceView):
    model = CalendarDay
    main_form = CalendarDayForm
    search_form = CalendarDaySearchForm
    list_template = 'calendar.html'
    detail_template = 'calendar-day.html'
    edit_template = 'calendar-day-edit.html'
    permissions = {
        'add': ('payroll.add_calendarday',),
        'edit': ('payroll.change_calendarday',)
    }


class HourTypeView(StandardResourceView):
    model = HourType
    main_form = HourTypeForm
    search_form = HourTypeSearchForm
    list_template = 'hour-types.html'
    detail_template = 'hour-type.html'
    edit_template = 'hour-type-edit.html'
    permissions = {
        'add': ('payroll.add_hourtype',),
        'edit': ('payroll.change_hourtype',)
    }


class PeriodView(StandardResourceView):
    model = Period
    main_form = PeriodForm
    search_form = PeriodSearchForm
    list_template = 'periods.html'
    detail_template = 'period.html'
    edit_template = 'period-edit.html'
    permissions = {
        'add': ('payroll.add_period',),
        'edit': ('payroll.change_period',)
    }

    def get_instance_context(self, request, obj, **kwargs):
        """
        Override to add worked hours subtotals.
        """
        # First get default context
        ctx = super(PeriodView, self).get_instance_context(request, obj)

        # Add worked hours and return context
        ctx['worked_hours'] = WorkedHours.objects.for_payroll(obj)\
            .group_by('hour_type').order_by('hour_type__id').annotate(total_hours=Sum('hours'))
        return ctx


class WorkedHoursView(SafeView):
    process_form = ProcessPayrollForm
    list_template = 'worked-hours.html'
    process_template = 'payroll-process.html'
    require_login = True
    permissions = {
        'process': ('payroll.add_workedhours',)
    }

    def get(self, request, period_pk, action=None):
        """
        HTTP GET request handler.
        """
        # Get period and build context
        period = Period.objects.get(id=period_pk)
        ctx = {'period': period}

        # Select template and update context based on action
        if action == 'process':
            # Process, add form to context
            ctx['form'] = self.process_form()
            template = self.process_template

        else:
            # Viewing the list, get queryset
            # Note: payroll period values are adj+act+fct
            worked_hours = WorkedHours.objects.for_payroll(period).consolidated()
            n_employees = WorkedHours.objects.for_payroll(period).group_by('employee').distinct().count()

            # Get pagination querystring and paginate accordingly
            page_size = request.GET.get('page_size') or 20
            page_num = request.GET.get('page', 1)
            # Note: result is generator, we need to make it Indexable
            p = Paginator(Indexable(worked_hours, length=n_employees), page_size)
            try:
                worked_hours = p.page(page_num)
            except PageNotAnInteger:
                worked_hours = p.page(1)
            except EmptyPage:
                worked_hours = p.page(p.num_pages)

            # Add to context and set template
            ctx['worked_hours'] = worked_hours
            ctx['hour_types'] = HourType.objects.for_user(request.user)
            template = self.list_template

        # Render template
        return render(request, template, ctx)

    def post(self, request, period_pk, action):
        """
        HTTP POST request handler.
        """
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
