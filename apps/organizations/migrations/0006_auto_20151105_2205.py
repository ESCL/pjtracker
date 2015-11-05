# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20151101_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='activities',
            field=models.ManyToManyField(blank=True, to='work.Activity'),
        ),
    ]
