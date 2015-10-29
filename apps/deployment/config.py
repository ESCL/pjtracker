__author__ = 'kako'

from django.apps import AppConfig


class MyAppConfig(AppConfig):

    name = 'apps.deployment'
    verbose_name = 'Deployment'

    def ready(self):
        from . import receivers