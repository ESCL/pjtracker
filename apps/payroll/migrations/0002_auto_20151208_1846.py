# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workedhours',
            name='phase',
            field=models.CharField(db_index=True, choices=[('D', 'Adjustment'), ('A', 'Actual'), ('F', 'Forecast'), ('R', 'Retroactive')], max_length=1),
        ),
    ]
