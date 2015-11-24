# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='code',
            field=models.CharField(max_length=16, unique=True, default='acc1', help_text='Short code used for users login.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=128, help_text='Full name to identify the account.'),
        ),
    ]
