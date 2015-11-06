__author__ = 'kako'

from django import forms

from ..common.forms import OwnedEntityForm
from ..work.models import Activity
from .models import TimeSheet, WorkLog


class TimeSheetForm(OwnedEntityForm):

    class Meta:
        model = TimeSheet
        fields = ('team', 'date',)

    def __init__(self, *args, instance=None, **kwargs):
        super(TimeSheetForm, self).__init__(*args, instance=instance, **kwargs)

        # Hide fields depending on whether it's new or not
        if instance:
            self.fields.pop('team')


class TeamActivityForm(OwnedEntityForm):

    def __init__(self, user, team, post_data=None):
        super(TeamActivityForm, self).__init__(post_data)

        allowed_activities = Activity.objects.for_user(user)
        self.fields['activities'] = forms.ModelMultipleChoiceField(
            queryset=allowed_activities,
            initial=team.activities.all()
        )


class WorkLogsForm(forms.Form):

    def __init__(self, post_data=None, instance=None, **kwargs):
        super(WorkLogsForm, self).__init__(post_data)
        self.timesheet = instance
        self.rows = []

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
                if not set(resource.allowed_labour_types).intersection(activity.allowed_labour_types):
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
                r_labour = resource.allowed_labour_types
                a_labour = activity.allowed_labour_types
                if not set(r_labour).intersection(a_labour):
                    if not r_labour:
                        es.append("{} cannot charge hours.".format(resource.instance))
                    if not a_labour:
                        es.append("Activity {} does not allow charging hours for any labour types.".format(activity))

                    if not es:
                        es.append("{} can charge hours as {}, activity {} only allows {}.".format(
                            resource, ', '.join(str(l) for l in r_labour), activity, ', '.join(str(l) for l in a_labour))
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
                log.labour_type = list(set(resource.allowed_labour_types).intersection(activity.allowed_labour_types))[0].value

                # Save the log
                log.save()

            else:
                # No hours, remove if existing
                if log.id:
                    log.delete()
