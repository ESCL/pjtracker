# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deployment', '0006_auto_20151106_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheetAction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('action', models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='issuer',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='reviewer',
        ),
        migrations.AddField(
            model_name='timesheetaction',
            name='timesheet',
            field=models.ForeignKey(to='deployment.TimeSheet', related_name='actions'),
        ),
    ]
