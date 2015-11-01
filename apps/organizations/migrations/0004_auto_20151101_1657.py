# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20151031_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='direct_labour',
        ),
        migrations.RemoveField(
            model_name='position',
            name='indirect_labour',
        ),
        migrations.RemoveField(
            model_name='position',
            name='managerial_labour',
        ),
    ]
