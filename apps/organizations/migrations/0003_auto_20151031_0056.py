# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_auto_20151031_0056'),
        ('organizations', '0002_team_supervisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='direct_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='indirect_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='managerial_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='activities',
            field=models.ManyToManyField(to='work.Activity'),
        ),
    ]
