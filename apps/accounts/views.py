from django.shortcuts import render

from ..common.exceptions import NotFoundError, NotAuthorizedError
from ..common.views.base import SafeView, StandardResourceView
from ..deployment.forms import TimeSheetSettingsForm
from ..payroll.forms import HoursSettingsForm
from .forms import UserForm, UserSearchForm
from .models import User


class SettingsView(SafeView):
    template_name = 'settings.html'
    required_permissions = (
        'deployment.change_timesheetsettings',
    )

    @classmethod
    def authorize(cls, request, action):
        if not request.user.owner:
            raise NotFoundError('The requested URL is not available.')

        all_perms = request.user.get_all_permissions()
        if not all_perms.intersection(cls.required_permissions):
            raise NotAuthorizedError('You are not authorized to edit account settings.')

    def get(self, request):
        account = request.user.owner
        ts_form = TimeSheetSettingsForm(instance=account.timesheet_settings)
        hs_form = HoursSettingsForm(account=account)

        context = {
            'account': account,
            'timesheets_form': ts_form,
            'hours_form': hs_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        account = request.user.owner

        ts_form = TimeSheetSettingsForm(request.POST, instance=account.timesheet_settings)
        hs_form = HoursSettingsForm(request.POST, account=account)
        if ts_form.is_valid() and hs_form.is_valid():
            ts_form.save()
            hs_form.save()

        context = {
            'account': account,
            'timesheets_form': ts_form,
            'hours_form': hs_form
        }
        return render(request, self.template_name, context)


class UserView(StandardResourceView):
    model = User
    include_global = False
    list_template = 'users.html'
    detail_template = 'user.html'
    edit_template = 'user-edit.html'
    search_form = UserSearchForm
    main_form = UserForm


