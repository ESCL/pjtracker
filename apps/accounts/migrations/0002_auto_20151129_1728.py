# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='owner',
            field=models.ForeignKey(blank=True, to='accounts.Account', related_name='users', null=True),
        ),
    ]
