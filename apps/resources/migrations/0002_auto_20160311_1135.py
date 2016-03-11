# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmenttype',
            name='code',
            field=models.CharField(max_length=4, default='LOL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmenttype',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='resource',
            name='project',
            field=models.ForeignKey(blank=True, null=True, to='work.Project'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='team',
            field=models.ForeignKey(blank=True, null=True, to='organizations.Team'),
        ),
    ]
