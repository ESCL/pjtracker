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


class WorkLogsForm(OwnedEntityForm):

    def __init__(self, post_data=None, instance=None, **kwargs):
        super(WorkLogsForm, self).__init__(post_data)
        self.timesheet = instance
        self.rows = []

        for employee in instance.employees.values():
            logs = []
            for activity in self.timesheet.activities.values():
                # Get log (existing or new)
                log = self._get_log_for(employee, activity)

                # Append to row and to form
                name = '{}.{}'.format(employee.id, activity.id)
                self.fields[name] = forms.DecimalField(
                    initial=log.hours, required=False, max_value=12
                )
                log.field = self[name]
                logs.append(log)

            self.rows.append({'employee': employee, 'logs': logs})

    def _iter_fields_values(self, cleaned_data):
        for fname, v in cleaned_data.items():
            e_id, a_id = fname.split('.')
            e = self.timesheet.employees[int(e_id)]
            a = self.timesheet.activities[int(a_id)]
            yield e, a, v

    def _get_log_for(self, employee, activity):
        return self.timesheet.work_logs_data.get(employee, {}).get(
            activity,
            WorkLog(timesheet=self.timesheet, employee=employee, activity=activity)
        )

    def clean(self):
        cleaned_data = super(WorkLogsForm, self).clean()

        for employee, activity, value in self._iter_fields_values(cleaned_data):
            if value:
                # Check that labour types match
                p_labour = {lt for lt in employee.position.labour_types if lt.allowed}
                a_labour = {lt for lt in activity.labour_types if lt.allowed}
                if not set(p_labour).intersection(a_labour):
                    es = []
                    if not p_labour:
                        es.append("Position {} does not allow charging hours.".format(employee.position))
                    if not a_labour:
                        es.append("Activity {} does not allow charging hours for any labour types.".format(activity))

                    if not es:
                        es.append("Employee {} can charge hours as {}, activity {} only allows {}.".format(
                            employee, ', '.join(str(l) for l in p_labour), activity, ', '.join(str(l) for l in a_labour))
                        )

                    raise forms.ValidationError(es)

        return cleaned_data

    def save(self):
        for employee, activity, value in self._iter_fields_values(self.cleaned_data):
            # Get log (existing or new)
            log = self._get_log_for(employee, activity)

            if value:
                # Some hours set, process the log
                log.hours = value

                # Use the first allowed labour type (we'll fix that later)
                # TODO: Allow setting labour type in timesheet
                p_labour = filter(lambda lt: lt.allowed, employee.position.labour_types)
                a_labour = filter(lambda lt: lt.allowed, activity.labour_types)
                log.labour_type = list(set(p_labour).intersection(a_labour))[0].value

                # Save the log
                log.save()

            else:
                # No hours, remove if existing
                if log.id:
                    log.delete()
