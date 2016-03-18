from django.shortcuts import render

from ..common.exceptions import NotAuthenticatedError, NotAuthorizedError
from ..common.views.base import SafeView, StandardResourceView
from ..deployment.forms import TimeSheetSettingsForm
from ..payroll.forms import HoursSettingsForm
from .forms import UserForm, UserSearchForm
from .models import User


class SettingsView(SafeView):
    """
    Account settings view, contains a few forms that define app behaviour
    for a few given parameters.
    """
    template_name = 'settings.html'
    required_permissions = (
        'deployment.change_timesheetsettings',
    )

    @classmethod
    def authorize(cls, request, action):
        """
        Check user permissions to authorize access or raise an error.
        """
        # Note: watch for anon, it has no owner attr
        if not getattr(request.user, 'owner', None):
            raise NotAuthenticatedError('The requested URL is not available.')

        all_perms = request.user.get_all_permissions()
        if not all_perms.intersection(cls.required_permissions):
            raise NotAuthorizedError('You are not authorized to edit account settings.')

    def get(self, request):
        """
        Render settings view.
        """
        # Get account and init forms
        account = request.user.owner
        ts_form = TimeSheetSettingsForm(instance=account.timesheet_settings)
        hs_form = HoursSettingsForm(account=account)

        # Build context and render template with it
        context = {
            'account': account,
            'timesheets_form': ts_form,
            'hours_form': hs_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Save all the settings form.
        """
        # Get account and init forms (with posted data)
        account = request.user.owner
        ts_form = TimeSheetSettingsForm(request.POST, instance=account.timesheet_settings)
        hs_form = HoursSettingsForm(request.POST, account=account)

        # Validate forms
        if ts_form.is_valid() and hs_form.is_valid():
            # All good, save them and set status to success
            ts_form.save()
            hs_form.save()
            status = 200

        else:
            # Error, set status to invalid
            status = 400

        # Build context and render template with it
        context = {
            'account': account,
            'timesheets_form': ts_form,
            'hours_form': hs_form
        }
        return render(request, self.template_name, context, status=status)


class UserView(StandardResourceView):
    model = User
    include_global = False
    list_template = 'users.html'
    detail_template = 'user.html'
    edit_template = 'user-edit.html'
    search_form = UserSearchForm
    main_form = UserForm


