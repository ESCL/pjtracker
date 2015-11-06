# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20151029_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmenttype',
            name='direct_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='indirect_labour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='managerial_labour',
            field=models.BooleanField(default=False),
        ),
    ]
