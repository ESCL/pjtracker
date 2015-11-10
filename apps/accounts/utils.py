__author__ = 'kako'

from django.contrib.auth.models import Permission, ContentType


def create_permissions(model, actions):
    ct = ContentType.objects.get_for_model(model)
    perms = []
    for action in actions:
        if ' ' in action:
            action, field = action.split(' ', 1)
            name = 'Can {} {} {}'.format(action.lower(), model._meta.verbose_name.lower(), field)
            codename = '{}_{}_{}'.format(action.lower(), model._meta.model_name, field.replace(' ', '_'))
        else:
            name = 'Can {} {}'.format(action.lower(), model._meta.verbose_name.lower())
            codename = '{}_{}'.format(action.lower(), model._meta.model_name)

        perms.append(Permission.objects.get_or_create(content_type=ct, name=name, codename=codename)[0])

    return perms