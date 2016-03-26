__author__ = 'kako'

from django.forms import ModelChoiceField


class CustomLabelModelChoiceField(ModelChoiceField):
    """
    ModelChoice field that allows defining the attribute to use for the
    options labels.
    """
    def __init__(self, *args, **kwargs):
        self.option_label_attr = kwargs.pop('option_label_attr')
        super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return getattr(obj, self.option_label_attr)
