# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20151203_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(max_length=1, default='E', choices=[('E', 'Active'), ('D', 'Dismissed'), ('X', 'Disabled')]),
        ),
    ]
