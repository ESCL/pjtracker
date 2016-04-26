# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0002_auto_20160416_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetaction',
            name='feedback',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='department',
            field=models.ForeignKey(null=True, blank=True, to='organizations.Department'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='equipment_type',
            field=models.ForeignKey(null=True, blank=True, to='resources.EquipmentType'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='location',
            field=models.ForeignKey(null=True, blank=True, to='geo.Location'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='position',
            field=models.ForeignKey(null=True, blank=True, to='organizations.Position'),
        ),
    ]
