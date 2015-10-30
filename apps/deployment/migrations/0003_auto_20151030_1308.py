# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0002_auto_20151029_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='issuer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='timesheets_issued', null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='reviewer',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='timesheets_reviewed', null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='status',
            field=models.CharField(max_length=1, default='P', choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')]),
        ),
    ]
