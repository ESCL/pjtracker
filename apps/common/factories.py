__author__ = 'claudio.melendrez'

from subfactory_propagated_fields import PropagatedFieldsSubFactory


def owned_subfactory(model):
    """
    Convenience method to return a PropagatedFieldsSubFactory for the given
    model with 'owner' as propagated field.

    :param model: model to use for
    :return: PropagatedFieldsSubFactory instance
    """
    return PropagatedFieldsSubFactory(model, propagated_fields=['owner'])
