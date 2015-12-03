# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='action_label',
            field=models.CharField(null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='notification',
            name='action_url',
            field=models.CharField(null=True, max_length=256),
        ),
    ]
