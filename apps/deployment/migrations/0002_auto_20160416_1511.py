# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('organizations', '0002_department'),
        ('deployment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='department',
            field=models.ForeignKey(null=True, to='organizations.Department'),
        ),
        migrations.AddField(
            model_name='worklog',
            name='location',
            field=models.ForeignKey(null=True, to='geo.Location'),
        ),
    ]
