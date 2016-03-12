# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20160301_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='code',
            field=models.CharField(default='LOL', max_length=4),
            preserve_default=False,
        ),
    ]
