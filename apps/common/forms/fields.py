__author__ = 'kako'

from django.forms import ModelChoiceField


class CustomLabelModelChoiceField(ModelChoiceField):
    """
    ModelChoice field that allows defining the attribute to use for the
    options labels.
    """
    def __init__(self, *args, option_label_attr=None, **kwargs):
        super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)
        self.option_label_attr = option_label_attr

    def label_from_instance(self, obj):
        return getattr(obj, self.option_label_attr)