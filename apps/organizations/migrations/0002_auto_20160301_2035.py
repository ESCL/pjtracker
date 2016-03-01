# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='position',
            name='code',
            field=models.CharField(null=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='team',
            name='code',
            field=models.CharField(max_length=8),
        ),
    ]
