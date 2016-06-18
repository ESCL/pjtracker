from django.apps import AppConfig


# Note: not sure why this class cannot contain suffix "Config"
class Common(AppConfig):
    name = 'apps.common'
