# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0003_auto_20151101_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='direct_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='indirect_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='managerial_labour',
            field=models.BooleanField(default=False),
        ),
    ]
