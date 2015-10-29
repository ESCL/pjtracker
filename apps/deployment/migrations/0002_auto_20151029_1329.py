# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deployment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='reviewer',
            field=models.ForeignKey(related_name='timesheets_reviewed', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='issuer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='timesheets_issued'),
        ),
    ]
