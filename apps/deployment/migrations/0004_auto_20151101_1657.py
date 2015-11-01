# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0003_auto_20151030_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='labour_type',
            field=models.CharField(choices=[('M', 'Managerial'), ('I', 'Indirect'), ('D', 'Direct')], max_length=1),
        ),
    ]
