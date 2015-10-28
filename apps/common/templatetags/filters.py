__author__ = 'kako'

import re

from django import template


register = template.Library()


@register.filter
def split_camelcase(value):
    """
    Split words in PascalCase into a sentence with the same case.

    :param value: word to split
    :return: sentence
    """
    return re.sub('([a-z])([A-Z])', '\g<1> \g<2>', value)
