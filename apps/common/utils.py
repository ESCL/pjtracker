__author__ = 'kako'

import re
import itertools


RE_NAME_REPLACE = re.compile(r'and|&|to|the|\W|\bI+\b', re.IGNORECASE)


def generate_code_from_name(name, min_len=2, max_len=3):
    """
    Generate a code from a bunch of words, such as position or team, trying to
    extract one or more chars from every word.

    Examples with min_len = 3:
      - "Some Name" -> "SON"
      - "What the Fuck" -> "WTF"
      - "Some Very Long Case" -> "SVL"
    """
    # First remove weird characters
    name = RE_NAME_REPLACE.sub(' ', name)

    # Now split in words
    name_parts = name.split()

    # Start by attaching at least one char from first word
    len_first = max(1, (min_len + 1) - len(name_parts))
    code_parts = [name_parts[0][:len_first]]

    # Now attach one char from every other word
    code_parts.extend(p[0] for p in name_parts[1:])

    # Return it upper-cased and truncated
    res = ''.join(code_parts).upper()[:max_len]
    return res


def generate_unique_code(instance, code_field, name_field, min_len=1, max_len=3):
    """
    Generate a unique code for the given container and field.

    :param instance: factory instance
    :param code_field: name of the target field for the code
    :param name_field: name of the field from which code is generated
    :param min_len: minimum length for code
    :param max_len: maximum length for code
    :return: new unique code
    """
    factory_cls = instance._LazyStub__model_class

    # First get and clean up name and split
    name = getattr(instance, name_field).lower()

    # Build unique query params
    unique_fields = set(factory_cls._meta.django_get_or_create)
    unique_fields.remove(code_field)
    kwargs = {fn: getattr(instance, fn) for fn in unique_fields if fn != code_field}

    # Attempt to generate code starting from min length to max
    while min_len <= max_len:
        # Generate code and set filter
        code = generate_code_from_name(name, min_len=min_len, max_len=max_len)
        kwargs[code_field] = code

        try:
            # Try to get an instance matching values
            existing_instance = factory_cls._meta.model.objects.get(**kwargs)

        except factory_cls._meta.model.DoesNotExist:
            # None exists, code is new
            return code

        else:
            # One exists, compare name field value, use code if it's the same
            if getattr(existing_instance, name_field).lower() == name:
                return code

        # Update new min length for next use
        min_len = len(code) + 1

    # Couldn't match it
    raise ValueError("Could not determine unique code for {}.".format(name))


class Indexable(object):
    """
    Wrapper to allow indexing (and thus, slicing) an iterator, that also
    caches the values as it iterates.
    """
    def __init__(self, iterator, length=100):
        self.iterator = iterator
        self.cache = []
        self.length = length

    def __iter__(self):
        for e in self.iterator:
            self.cache.append(e)
            yield e

    def __getitem__(self, index):
        try:
            max_idx = index.stop

        except AttributeError:
            max_idx = index

        n = max_idx - len(self.cache) + 1
        if n > 0:
            self.cache.extend(itertools.islice(self.iterator, n))
        return self.cache[index]

    def __len__(self):
        return self.length