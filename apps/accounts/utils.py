__author__ = 'kako'

from django.contrib.auth.models import Permission, ContentType


def build_username(username, owner):
    """
    Build a username including the owner account's code if it has one,
    in the format <user>@<account>.

    # Note: we moved this out of User class to allow using it in migrations.
    """
    proper_username = username.split('@')[0]
    if proper_username and owner:
        proper_username += '@{}'.format(owner.code)
    return proper_username


def ensure_permissions(model, actions, permission_model=Permission):
    """
    Ensure the existence of a set of permissions defined by a model and a set
    of actions, and optionally a versioned permission model (for migrations).

    :param model: model for permission
    :param actions: set of actions (change, add, delete)
    :param permission_model: versioned permission model
    :return: list of matching permissions
    """
    # Get model content type, start with empty list of permissions
    ct = ContentType.objects.get_for_model(model)
    perms = []

    # Iterate actions
    for action in actions:
        # Build name and codename for permission
        if ' ' in action:
            # Permission for model field (eg, "change activities")
            action, field = action.split(' ', 1)
            name = 'Can {} {} {}'.format(action.lower(), model._meta.verbose_name.lower(), field)
            codename = '{}_{}_{}'.format(action.lower(), model._meta.model_name, field.replace(' ', '_'))
        else:
            # Permission for whole model (eg, "change", "delete")
            name = 'Can {} {}'.format(action.lower(), model._meta.verbose_name.lower())
            codename = '{}_{}'.format(action.lower(), model._meta.model_name)

        # Get or create permission, append to list
        perm = permission_model.objects.get_or_create(
            content_type_id=ct.id, name=name, codename=codename
        )[0]
        perms.append(perm)

    # Return list of permissions
    return perms
