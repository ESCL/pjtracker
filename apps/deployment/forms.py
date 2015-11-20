__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm, ModernForm
from .models import TimeSheet, WorkLog


class TimeSheetForm(OwnedEntityForm):

    class Meta:
        model = TimeSheet
        fields = ('team', 'date',)

    def __init__(self, *args, **kwargs):
        super(TimeSheetForm, self).__init__(*args, **kwargs)

        # Remove team field for existing timesheets (resources depend on this so
        # we can't have people changing it)
        if kwargs.get('instance'):
            self.fields.pop('team')

    def clean(self):
        cleaned_data = super(TimeSheetForm, self).clean()
        if not self.instance.id:
            # New timesheet, ensure it is not a duplicate (team:date)
            team = cleaned_data.get('team')
            date = cleaned_data['date']

            if TimeSheet.objects.filter(team=team, date=date).exists():
                cleaned_data.pop('team')
                cleaned_data.pop('date')
                raise forms.ValidationError('TimeSheet for team {} and date {} already exists.'.format(team, date))

        return cleaned_data


class TimeSheetSearchForm(ModernForm):
    team__code__icontains = forms.CharField(max_length=32, required=False, label='Team code')
    date__gte = forms.DateField(label='From date')
    date__lte = forms.DateField(label='Until date')


class TimeSheetActionForm(forms.Form):

    action = forms.ChoiceField()
    feedback = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(TimeSheetActionForm, self).__init__(*args, **kwargs)

        # Add choices to actions based on current status
        instance = kwargs.get('instance')
        self.fields['action'].choices = instance.allowed_actions

        # Store user and timesheet for future ref
        self.timesheet = instance
        self.user = kwargs.get('user')

    def clean(self):
        cleaned_data = super(TimeSheetActionForm, self).clean()

        # Make sure we include feedback for rejections
        action = cleaned_data.get('action')
        feedback = cleaned_data.get('feedback')
        if action == 'reject' and not feedback:
            raise forms.ValidationError("Feedback is required for rejections to "
                                        "help timekeepers correct any mistakes.")

        return cleaned_data

    def save(self):
        action = self.cleaned_data.get('action')
        method = getattr(self.timesheet, action)
        method(self.user)


class WorkLogsForm(forms.Form):

    def __init__(self, post_data=None, instance=None, user=None, **kwargs):
        super(WorkLogsForm, self).__init__(post_data)
        self.timesheet = instance
        self.rows = []
        self.user = user

        for pk, resource in self.timesheet.resources.items():
            logs = []
            for activity in self.timesheet.activities.values():
                # Get log (existing or new)
                log = self._get_log_for(resource, activity)

                # Append to row and to form
                name = '{}.{}'.format(pk, activity.id)
                self.fields[name] = forms.DecimalField(
                    initial=log.hours, required=False, max_value=12,
                )
                res_lt = resource.get_labour_types_for(self.user)
                act_lt = activity.labour_types.all()
                if not set(res_lt).intersection(act_lt):
                    self.fields[name].widget.attrs.update({'disabled': 'disabled',
                                                           'readonly': True})
                log.field = self[name]
                logs.append(log)

            self.rows.append({'resource': resource, 'logs': logs})

    def _get_log_for(self, resource, activity):
        return self.timesheet.work_logs_data.get(resource, {}).get(
            activity,
            WorkLog(timesheet=self.timesheet, resource=resource, activity=activity)
        )

    def _iter_fields_values(self, cleaned_data):
        for fname, v in cleaned_data.items():
            r_id, a_id = fname.split('.')
            r = self.timesheet.resources[int(r_id)]
            a = self.timesheet.activities[int(a_id)]
            yield r, a, v

    def clean(self):
        cleaned_data = super(WorkLogsForm, self).clean()
        es = []

        for resource, activity, value in self._iter_fields_values(cleaned_data):
            if value:
                # Check that labour types match
                res_lt = resource.get_labour_types_for(self.user)
                act_lt = activity.labour_types.all()
                if not set(res_lt).intersection(act_lt):
                    if not res_lt.exists():
                        es.append("{} cannot charge hours.".format(resource.instance))
                    if not act_lt.exists():
                        es.append("Activity {} does not allow charging hours for any labour types.".format(activity))

                    if not es:
                        es.append("{} can charge hours as {}, activity {} only allows {}.".format(
                            resource, ', '.join(str(l) for l in res_lt), activity, ', '.join(str(l) for l in act_lt))
                        )

        if es:
            raise forms.ValidationError(es)
        return cleaned_data

    def save(self):
        for resource, activity, value in self._iter_fields_values(self.cleaned_data):
            # Get log (existing or new)
            log = self._get_log_for(resource, activity)

            if value:
                # Some hours set, process the log
                log.hours = value

                # Use the first allowed labour type (we'll fix that later)
                # TODO: Allow setting labour type in timesheet
                res_lt = resource.get_labour_types_for(self.user)
                act_lt = activity.labour_types.all()
                log.labour_type = list(set(res_lt).intersection(act_lt))[0]

                # Save the log
                log.save()

            else:
                # No hours, remove if existing
                if log.id:
                    log.delete()


class HoursSearchForm(ModernForm):
    from_date = forms.DateField(label='From date', required=False)
    to_date = forms.DateField(label='To date', required=False)
    status = forms.ChoiceField(
        label='Time-sheet status', required=False,
        choices=((None, 'All'),
                 ('approved', 'Approved'),
                 ('issued', 'Issued')),
        initial=None
    )
    group_by = forms.ChoiceField(
        label='Grouping options',
        widget=forms.CheckboxSelectMultiple,
        choices=(('project', 'Project'),
                 ('activity', 'Activity'),
                 ('labour_type', 'Labour type'),
                 ('resource', 'Resource')),
        initial=['project']
    )