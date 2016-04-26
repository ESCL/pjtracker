__author__ = 'kako'

import logging

from django.contrib.sessions.models import Session


logger = logging.getLogger()


def validate_model_save(sender, instance, *args, **kwargs):
    # Ignore django session because there's a bug in test client login
    if not isinstance(instance, Session):
        try:
            instance.full_clean()
        except Exception as e:
            logger.debug('Cannot save {}: {}'.format(instance, e))
            raise
