__author__ = 'claudio.melendrez'

from factory import SubFactory


class PropagatedFieldsSubFactory(SubFactory):
    """
    SubFactory that takes the value of the "propagated_fields" to populate
    its own fields with the same values.
    """
    def __init__(self, *args, **kwargs):
        """
        Store the propagated fields iterable.
        """
        self._propagated_fields = kwargs.pop('propagated_fields', [])
        super(PropagatedFieldsSubFactory, self).__init__(*args, **kwargs)

    def generate(self, sequence, obj, create, params):
        """
        Fill the params with all the propagated values from parent factory.
        """
        for f in self._propagated_fields:
            params[f] = getattr(obj, f, None)

        return super(PropagatedFieldsSubFactory, self).generate(sequence, obj,
                                                                create, params)


def owned_subfactory(model):
    """
    Convenience method to return a PropagatedFieldsSubFactory for the given
    model with 'owner' as propagated field.

    :param model: model to use for
    :return: PropagatedFieldsSubFactory instance
    """
    return PropagatedFieldsSubFactory(model, propagated_fields=['owner'])
