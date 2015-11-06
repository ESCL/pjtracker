# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20151029_1329'),
        ('deployment', '0005_auto_20151106_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='equipment_type',
            field=models.ForeignKey(null=True, to='resources.EquipmentType'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='position',
            field=models.ForeignKey(null=True, to='organizations.Position'),
        ),
    ]
