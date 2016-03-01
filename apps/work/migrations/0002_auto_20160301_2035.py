# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='activitygroup',
            name='code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='activitygroup',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(max_length=8),
        ),
    ]
