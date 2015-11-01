# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20151101_1657'),
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
    ]
