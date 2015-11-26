__author__ = 'kako'

import re


RE_NAME_REPLACE = re.compile(r'[\(\)-/]')
LEVEL_REPLACE = re.compile(r'\bI+\b')


def generate_code_from_name(name, max_len=3):
    """
    Generate a code from a bunch of words, such as position or team, trying to
    extract one or more chars from every word.

    Examples:
      - "Some Name" -> "SON"
      - "What the Fuck" -> "WTF"
      - "Some Very Long Case" -> "SVL"
    """
    # First remove weird characters
    name = RE_NAME_REPLACE.sub('', name.replace('/', ' '))
    name = LEVEL_REPLACE.sub('', name)

    # Now split in words
    name_parts = name.split()

    # Start by attaching at least one char from first word
    len_first = max(1, (max_len + 1) - len(name_parts))
    code_parts = [name_parts[0][:len_first]]

    # Now attach one char from every other word
    code_parts.extend(p[0] for p in name_parts[1:])

    # Return it upper-cased and truncated
    return ''.join(code_parts).upper()[:max_len]
