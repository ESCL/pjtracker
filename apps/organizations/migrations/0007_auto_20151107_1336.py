# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0006_auto_20151105_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='team',
            name='supervisors',
            field=models.ManyToManyField(related_name='supervised_teams', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='timekeepers',
            field=models.ManyToManyField(related_name='timekept_teams', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
