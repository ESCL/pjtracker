__author__ = 'kako'

from django import template

register = template.Library()


@register.assignment_tag
def get(instance, method_name, *args, **kwargs):
    """
    Generic tag to run any get_ method on any instance with any parameters.
    Since get_ methods are (usually) nothing but getters with parameters,
    we shouldn't worry (too much).
    """
    return getattr(instance, 'get_{}'.format(method_name))(*args, **kwargs)
