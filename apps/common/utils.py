__author__ = 'kako'

import re


RE_NAME_REPLACE = re.compile(r'[\(\)-/]')


def generate_code_from_name(name, max_len=3):
    """
    Generate a code from a bunch of words, such as position or team, trying to
    extract one or more chars from every word.

    Examples:
      - "Some Name" -> "SON"
      - "What the Fuck" -> "WAF" (yes, "the" is too short and is ignored)
      - "Some Very Long Case" -> "SVL"
    """
    # First remove weird characters
    name = RE_NAME_REPLACE.sub('', name.replace('/', ' '))

    # Now split in words
    name_parts = [p for p in name.split() if len(p) > 3]

    # Start by attaching at least one char from first word
    len_first = max(1, (max_len + 1) - len(name_parts))
    code_parts = [name_parts[0][:len_first]]

    # Now attach one char from every other word
    code_parts.extend(p[0] for p in name_parts[1:])

    # Return it upper-cased and truncated
    return ''.join(code_parts).upper()[:max_len]
