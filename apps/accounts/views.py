from django.shortcuts import render

from ..common.views.base import SafeView, StandardResourceView
from ..deployment.forms import TimeSheetSettingsForm
from .forms import UserForm, UserSearchForm
from .models import User


class SettingsView(SafeView):
    template_name = 'settings.html'

    def get(self, request):
        account = request.user.owner

        ts_form = TimeSheetSettingsForm(instance=account.timesheet_settings)

        context = {
            'account': account,
            'timesheets_form': ts_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        account = request.user.owner

        ts_form = TimeSheetSettingsForm(request.POST, instance=account.timesheet_settings)
        if ts_form.is_valid():
            ts_form.save()

        context = {
            'account': account,
            'timesheets_form': ts_form
        }
        return render(request, self.template_name, context)


class UserView(StandardResourceView):
    model = User
    list_template = 'users.html'
    detail_template = 'user.html'
    edit_template = 'user-edit.html'
    search_form = UserSearchForm
    main_form = UserForm
    # Go back to settings on save
    collection_view_name = 'settings'
