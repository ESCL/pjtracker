# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='code',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
