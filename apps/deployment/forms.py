__author__ = 'kako'

from django import forms


class EmployeeWorkLogsForm(forms.Form):

    def __init__(self, employee, activities, post_data):
        super(EmployeeWorkLogsForm, self).__init__(post_data)

        self.fields['employee'] = forms.ChoiceField(widget=forms.HiddenInput)
        for activity in activities:
            self.fields['activity-{}'.format(activity.id)] = forms.DecimalField()
