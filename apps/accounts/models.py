from django.db import models


class Account(models.Model):

    name = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    TYPE_ADMIN = 'A'
    TYPE_USER = 'U'

    user = models.OneToOneField(
        'auth.User',
        related_name='profile'
    )
    account = models.ForeignKey(
        'Account'
    )
    account_role = models.CharField(
        max_length=1,
        choices=((TYPE_ADMIN, 'Administrator'),
                 (TYPE_USER, 'Common'))
    )

    def __str__(self):
        return self.account.name
