__author__ = 'kako'

from factory import SubFactory, SelfAttribute


class NullableSubFactory(SubFactory):
    """
    SubFactory for nullable foreign key relationships, which does not
    generate an object when no data is provided.
    """
    def generate(self, sequence, obj, create, params):
        """
        Override SubFactory generation to allow using None as value
        when no subfactory fields are provided.
        """
        validate = params.pop('validate', False)

        # Check all params on generation
        for k, v in params.items():
            if not(k.startswith('__') or isinstance(v, SelfAttribute)):
                # Value provided for at least one field, generate instance
                res = super(NullableSubFactory, self).generate(sequence, obj, create, params)
                if validate:
                    res.full_clean()
                return res

        # No data for object creation, return None
        return None
