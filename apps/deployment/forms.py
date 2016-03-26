__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from ..common.forms.fields import CustomLabelModelChoiceField
from ..common.forms.mixins import PagedForm
from .models import TimeSheet, WorkLog, TimeSheetSettings


class TimeSheetSettingsForm(forms.ModelForm):

    class Meta:
        model = TimeSheetSettings
        exclude = ('account',)

    def clean(self):
        """
        Make sure review policies are compatible to avoid status resolution
        limbo, which is defined as ALL is only compatible with FIRST.
        """
        cleaned_data = super(TimeSheetSettingsForm, self).clean()

        # Get values for approval and rejection policies
        app_pol = cleaned_data.get('approval_policy')
        rej_pol = cleaned_data.get('rejection_policy')

        # If we have nothing return, form's already invalid
        if not (app_pol or rej_pol):
            return

        # Now make sure policies are compatible
        policies = {app_pol, rej_pol}
        if TimeSheet.REVIEW_POLICY_ALL in policies and \
                TimeSheet.REVIEW_POLICY_FIRST not in policies:
            # They are not, error
            cleaned_data.pop('approval_policy')
            cleaned_data.pop('rejection_policy')
            raise forms.ValidationError(
                'This combination is not allowed because time-sheet status '
                'can remain undefined after all reviews have been submitted.'
            )

        return cleaned_data


class TimeSheetForm(OwnedEntityForm):

    class Meta:
        model = TimeSheet
        fields = ('team', 'date', 'comments',)

    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(TimeSheetForm, self).__init__(*args, **kwargs)

        # Remove team field for existing timesheets (resources depend on this so
        # we can't have people changing it)
        if self.instance.id:
            self.fields.pop('team', None)
        else:
            self.fields.pop('comments', None)

    def clean(self):
        cleaned_data = super(TimeSheetForm, self).clean()
        if not self.instance.id:
            # New timesheet, ensure it is not a duplicate (team:date)
            team = cleaned_data.get('team')
            date = cleaned_data['date']
            if TimeSheet.objects.filter(team=team, date=date).exists():
                cleaned_data.pop('team')
                cleaned_data.pop('date')
                raise forms.ValidationError('TimeSheet for team {} and date {} '
                                            'already exists.'.format(team, date))

        return cleaned_data

    def save(self, commit=True):
        if not self.instance.owner:
            self.instance.owner = self.instance.team.owner
        return super(TimeSheetForm, self).save(commit=commit)


class TimeSheetSearchForm(ModernForm, PagedForm):
    team__code__icontains = forms.CharField(max_length=32, required=False,
                                            label='Team code')
    date__gte = forms.DateField(label='From date')
    date__lte = forms.DateField(label='Until date')


class TimeSheetActionForm(forms.Form):

    # Action choices are empty, they are defined on form init
    action = forms.ChoiceField()
    feedback = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        # Pop user/ts first to avoid superclass errors
        self.user = kwargs.pop('user', None)
        self.timesheet = kwargs.pop('instance', None)

        # Now init form to create all fields
        super(TimeSheetActionForm, self).__init__(*args, **kwargs)

        # Add choices to actions based on current status
        self.fields['action'].choices = self.timesheet.allowed_actions

    def clean(self):
        cleaned_data = super(TimeSheetActionForm, self).clean()

        # Make sure we include feedback for rejections
        action = cleaned_data.get('action')
        feedback = cleaned_data.get('feedback')
        if action == 'reject' and not feedback:
            cleaned_data.pop('feedback', None)

            # Add the error to feedback field specifically
            self.add_error(
                'feedback',
                forms.ValidationError("Feedback is required for rejections to "
                                      "help timekeepers correct any mistakes.")
            )

        return cleaned_data

    def save(self):
        # Determine method and execute it
        action = self.cleaned_data.get('action')
        method = getattr(self.timesheet, action)
        method(self.user)


class WorkLogsForm(forms.Form):

    def __init__(self, post_data=None, instance=None, user=None, **kwargs):
        """
        Build the form fields by using the instance's resources and activities,
        generating alerts if any issues are detected.

        :param post_data: posted form data (dict-like object)
        :param instance: TimeSheet instance
        :param user: User instance interacting with the form
        """
        # Note: this is way too long, we need to move some logic out
        super(WorkLogsForm, self).__init__(post_data, **kwargs)
        self.timesheet = instance
        self.rows = []
        self.alerts = []
        self.user = user

        # Sanity checks
        lts_matched = False
        has_acts = bool(self.timesheet.activities)
        has_res = bool(self.timesheet.resources)

        # Main processing
        for pk, resource in self.timesheet.resources.items():
            logs = []

            # Get labour types for resource and add lt choice field
            # Note: this won't scale, we need to move this out and do a
            # single query
            res_lt = resource.get_labour_types_for(self.user)
            self.fields[str(resource.id)] = CustomLabelModelChoiceField(
                queryset=res_lt, option_label_attr='code', empty_label=None,
            )

            # Now add work log fields
            for activity in self.timesheet.activities.values():
                # Get log (existing or new)
                log = self._get_log_for(resource, activity)

                # Generate field
                log_name = '{}.{}'.format(pk, activity.id)
                self.fields[log_name] = forms.DecimalField(
                    initial=log.hours, required=False, max_value=12,
                )

                # Disable if labour types don't match
                act_lt = activity.labour_types.all()
                if not set(res_lt).intersection(act_lt):
                    self.fields[log_name].widget.attrs.update(
                        {'disabled': 'disabled', 'readonly': True}
                    )

                elif not lts_matched:
                    lts_matched = True

                # Attach to log and form
                log.field = self[log_name]
                logs.append(log)

            self.rows.append({'resource': resource,
                              'labour_type': self[str(resource.id)],
                              'logs': logs})

        # Append alerts if we have any problems
        if not has_res:
            self.alerts.append('This team has no resources assigned.')
        if not has_acts:
            self.alerts.append('This team has no activities assigned.')

        if has_acts and has_res and not lts_matched:
            self.alerts.append('Labour types for activities and resources '
                               'assigned to this team do not match.')

    def _get_log_for(self, resource, activity):
        """
        Get a WorkLog for the given resource and activity for this timesheet,
        which might be a stored one or a new one.

        :param resource: Resource instance
        :param activity: Activity instance
        :return: WorkLog instance (existing or new)
        """
        return self.timesheet.work_logs_data.get(resource, {}).get(
            activity,
            WorkLog(timesheet=self.timesheet, resource=resource, activity=activity)
        )

    def _iter_fields_values(self, cleaned_data):
        """
        Iterate field values sorted by their field name, matching the sorting
        in the template (top resources first, bottom last).

        :param cleaned_data: dict with form cleaned data (validated)
        :yield: tuple of Resource, Activity, hours
        """
        for fname, v in sorted(cleaned_data.items()):
            if '.' in fname:
                r_id, a_id = fname.split('.')
                r = self.timesheet.resources[int(r_id)]
                a = self.timesheet.activities[int(a_id)]
                yield r, a, v

    def clean(self):
        """
        Ensure that selected labour types match the labour types allowed
        for the activiesy.
        """
        cleaned_data = super(WorkLogsForm, self).clean()
        es = []

        for resource, activity, value in self._iter_fields_values(cleaned_data):
            if value:
                # Check that labour types match
                # Note: yes, I know we disable inputs, still
                res_lt = self.cleaned_data.get(str(resource.id))
                act_lt = set(activity.labour_types.all())

                # Note: in theory the messages below ARE NOT mutually exclusive,
                # but displaying more than one per field is too much, so we
                # sort them by relevance
                if not res_lt:
                    es.append("{} cannot charge hours.".format(resource.instance))

                elif not act_lt:
                    es.append("Activity {} does not allow charging "
                              "hours.".format(activity))

                elif res_lt not in act_lt:
                    es.append("Activity {} does not allow charging hours "
                              "for {}.".format(activity, res_lt))

        if es:
            raise forms.ValidationError(es)

        return cleaned_data

    def save(self):
        """
        Save all the resource:activity combinations, which might require an
        update (if saved hours > 0), a new instance (if not existing) or
        deleting one (saved hours > 0 and new hours = 0).
        """
        for resource, activity, value in self._iter_fields_values(self.cleaned_data):
            # Get log (existing or new)
            log = self._get_log_for(resource, activity)

            if value:
                # Some hours set, process the log and save it
                log.hours = value
                log.labour_type = self.cleaned_data[str(resource.id)]
                log.save()

            else:
                # No hours, remove if existing
                if log.id:
                    log.delete()


class HoursSearchForm(ModernForm, PagedForm):
    # Filters
    from_date = forms.DateField(label='From date', required=False)
    to_date = forms.DateField(label='To date', required=False)
    status = forms.ChoiceField(
        label='Time-sheet status', required=False,
        choices=((None, 'All time-sheets'),
                 ('approved', 'Approved'),
                 ('issued', 'Issued'))
    )
    resource_type = forms.ChoiceField(
        label='Resource type', required=False,
        choices=((None, 'All resources'),
                 ('employee', 'Employees'),
                 ('equipment', 'Equipment'))
    )

    # Group by options
    group_by = forms.ChoiceField(
        label='Grouping options',
        widget=forms.CheckboxSelectMultiple,
        choices=(('project', 'Project'),
                 ('activity', 'Activity'),
                 ('labour_type', 'Labour type'),
                 ('resource', 'Resource'),
                 ('date', 'Date'))
    )
