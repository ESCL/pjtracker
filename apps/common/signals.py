__author__ = 'kako'


class SignalsMixin(object):
    """
    Provide generic, simplified signal connection and sending mechanisms,
    similar to JavaScript.
    By default uses the generic signals provided for all
    """
    SIGNALS = {}

    @classmethod
    def on_signal(cls, type, receiver):
        """
        Connect the given receiver to the signal of the given type, raising
        an error if the type doesn't exist.
        """
        signal = cls.SIGNALS.get(type.lower())
        if not signal:
            raise TypeError("No signal found for event type '{}'.".format(type))

        uid = '{}-{}'.format(cls.__name__, type)
        signal.connect(receiver, sender=cls, dispatch_uid=uid)

    def signal(self, type, **kwargs):
        """
        Send the signal of the given type if, raising an error if the type
        doesn't exist.
        """
        signal = self.SIGNALS.get(type.lower())
        if not signal:
            raise TypeError("No signal found for event type '{}'.".format(type))

        signal.send(sender=self.__class__, target=self, type=type, **kwargs)

