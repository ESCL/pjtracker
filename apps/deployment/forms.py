__author__ = 'kako'

from django import forms

from ..work.models import Activity
from .models import TimeSheet, WorkLog


class TimeSheetForm(forms.ModelForm):

    class Meta:
        model = TimeSheet
        fields = ('team', 'date',)

    def __init__(self, *args, instance=None, **kwargs):
        super(TimeSheetForm, self).__init__(*args, instance=instance, **kwargs)

        # Hide fields depending on whether it's new or not
        if instance:
            self.fields.pop('team')


class TeamActivityForm(forms.Form):

    def __init__(self, user, team, post_data=None):
        super(TeamActivityForm, self).__init__(post_data)

        allowed_activities = Activity.objects.for_user(user)
        self.fields['activities'] = forms.ModelMultipleChoiceField(
            queryset=allowed_activities,
            initial=team.activities.all()
        )


class WorkLogsForm(forms.Form):

    def __init__(self, timesheet, post_data=None):
        super(WorkLogsForm, self).__init__(post_data)
        self.rows = []
        for employee in timesheet.employees:
            logs = []
            for activity in timesheet.activities:
                # Get existing or new log for activity
                log = timesheet.work_logs_data.get(employee, {}).get(
                    activity,
                    WorkLog(timesheet=timesheet, employee=employee)
                )

                # Append to row and to form
                name = '{}.{}'.format(employee.id, activity.id)
                self.fields[name] = forms.DecimalField(initial=log.hours)
                log.field = self[name]
                logs.append(log)

            self.rows.append({'employee': employee, 'logs': logs})
