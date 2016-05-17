# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_create_defaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='activitygrouptype',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
