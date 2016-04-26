# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='location',
            field=models.ForeignKey(blank=True, to='geo.Location', null=True),
        ),
    ]
