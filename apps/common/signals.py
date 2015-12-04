__author__ = 'kako'

from django.db.models.signals import post_save, post_delete


class SignalsMixin(object):
    """
    Provide generic, simplified signal connection and sending mechanisms to
    Django models, somewhat inspired by JavaScript events.

    By default adds 'saved' and 'deleted' signals ready to use, and more can
    be added by overriding the CUSTOM_SIGNALS dictionary. All sent signals
    pass the model instance as the 'instance' parameter, and custom ones
    also pass a 'name', which is the key in CUSTOM_SIGNALS.

    Example use:
        class SomeModel(models.Model, SignalsMixin):
            CUSTOM_SIGNALS = {'viewed': Signal()}
            ...
            def mark_as_viewed(self):
                self.status = 'viewed'
                self.save()
                self.signal('viewed')

        SomeModel.on_signal('saved', do_something)
        SomeModel.on_signal('viewed', do_something_else)
    """
    _DEFAULT_SIGNALS = {
        'saved': post_save,
        'deleted': post_delete
    }
    CUSTOM_SIGNALS = {}

    @classmethod
    def _get_signal(cls, name):
        """
        Get the signal with the given name in defaults or custom signals.
        """
        signal = cls._DEFAULT_SIGNALS.get(name)
        if not signal:
            signal = cls.CUSTOM_SIGNALS.get(name)

        if not signal:
            raise TypeError("No signal named '{}' found for {}.".format(name, cls))

        return signal

    @classmethod
    def on_signal(cls, name, receiver):
        """
        Connect the given receiver to the signal of the given type, raising
        an error if the type doesn't exist.
        """
        signal = cls._get_signal(name)
        uid = '{}.{}.{}'.format(cls._meta.model_name, name, receiver.__name__)
        signal.connect(receiver, sender=cls, dispatch_uid=uid)

    def signal(self, name, **kwargs):
        """
        Send the signal of the given type if, raising an error if the type
        doesn't exist.
        """
        signal = self._get_signal(name)
        signal.send(sender=self.__class__, instance=self, name=name, **kwargs)

