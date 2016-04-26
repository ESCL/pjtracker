# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20160416_2144'),
        ('deployment', '0003_auto_20160416_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='category',
            field=models.ForeignKey(blank=True, null=True, to='resources.ResourceCategory'),
        ),
    ]
