# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyhistory',
            name='team',
        ),
        migrations.RemoveField(
            model_name='positionhistory',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='positionhistory',
            name='position',
        ),
        migrations.RemoveField(
            model_name='projecthistory',
            name='team',
        ),
        migrations.RemoveField(
            model_name='teamhistory',
            name='team',
        ),
        migrations.DeleteModel(
            name='CompanyHistory',
        ),
        migrations.DeleteModel(
            name='PositionHistory',
        ),
        migrations.DeleteModel(
            name='ProjectHistory',
        ),
        migrations.DeleteModel(
            name='TeamHistory',
        ),
    ]
