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


@register.simple_tag
def lookup(dict_value, key, default=None):
    """
    Lookup a key in a dictionary and return the stored value, or None if not found.

    :param dict_value: dictionary
    :param key: target key
    :return: target value or None
    """
    return dict_value.get(key, default)
