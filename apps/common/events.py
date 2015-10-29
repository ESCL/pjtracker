__author__ = 'kako'

from django.dispatch import Signal


SIGNALS = {
    'issued': Signal(providing_args=['target']),
    'approved': Signal(providing_args=['target']),
    'rejected': Signal(providing_args=['target']),
    'read': Signal(providing_args=['target'])
}


class SignalerMixin(object):
    """
    Provide generic, simplified signal connection and sending mechanisms,
    similar to JavaScript.
    """
    @classmethod
    def on_signal(cls, type, receiver):
        """
        Connect the given receiver to the signal of the given type, raising
        an error if the type doesn't exist.
        """
        signal = SIGNALS.get(type.lower())
        if not signal:
            raise TypeError("No signal found for event type '{}'.".format(type))

        uid = '{}-{}'.format(cls.__name__, type)
        signal.connect(receiver, sender=cls, dispatch_uid=uid)

    def signal(self, type, **kwargs):
        """
        Send the signal of the given type if, raising an error if the type
        doesn't exist.
        """
        signal = SIGNALS.get(type.lower())
        if not signal:
            raise TypeError("No signal found for event type '{}'.".format(type))

        signal.send(sender=self.__class__, target=self, type=type, **kwargs)

