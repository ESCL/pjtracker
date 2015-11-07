# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0008_auto_20151107_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsettings',
            name='account',
            field=models.OneToOneField(to='accounts.Account', related_name='timesheet_settings'),
        ),
    ]
