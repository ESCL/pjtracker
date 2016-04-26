# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20160416_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcecategory',
            options={'verbose_name_plural': 'resource categories'},
        ),
    ]
