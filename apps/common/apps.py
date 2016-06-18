from django.apps import AppConfig
from django.db.models.signals import pre_save


class Common(AppConfig):
    name = 'apps.common'

    def ready(self):
        from .signals import validate_model_save
        pre_save.connect(validate_model_save, dispatch_uid='asdkasdi')
