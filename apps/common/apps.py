
from django.apps import AppConfig
from django.db.models.signals import pre_save

from .signals import validate_model_save


class Common(AppConfig):
    name = 'apps.common'
    verbose_name = "common"

    def ready(self):
        pre_save.connect(validate_model_save, dispatch_uid='asdkasdi')
