# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='model',
            field=models.CharField(default='Komatsu D2450', help_text='Manufacturer brand and model.', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='year',
            field=models.PositiveIntegerField(default=2005, help_text='Year of manufacture.'),
            preserve_default=False,
        ),
    ]
