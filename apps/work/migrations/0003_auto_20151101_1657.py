# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_auto_20151031_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='direct_labour',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='indirect_labour',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='managerial_labour',
        ),
    ]
