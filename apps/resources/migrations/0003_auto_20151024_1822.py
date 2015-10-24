# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20151024_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='parent',
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='parent',
            field=models.ForeignKey(null=True, related_name='subtypes', to='resources.EquipmentType'),
        ),
    ]
