# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20151029_1329'),
        ('deployment', '0004_auto_20151101_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worklog',
            name='employee',
        ),
        migrations.AddField(
            model_name='worklog',
            name='resource',
            field=models.ForeignKey(to='resources.Resource', default=1),
            preserve_default=False,
        ),
    ]
