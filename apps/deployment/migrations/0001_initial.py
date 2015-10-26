# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('work', '__first__'),
        ('resources', '__first__'),
        ('geo', '__first__'),
        ('organizations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=1, choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')])),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(null=True, max_length=256, blank=True)),
                ('issuer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, blank=True, to='accounts.Account')),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('labour_type', models.CharField(max_length=1, choices=[('I', 'Indirect'), ('D', 'Direct'), ('M', 'Managerial')])),
                ('hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('activity', models.ForeignKey(null=True, blank=True, to='work.Activity')),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('employee', models.ForeignKey(to='resources.Employee')),
                ('location', models.ForeignKey(to='geo.Location')),
                ('position', models.ForeignKey(to='resources.Position')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='work_logs')),
            ],
        ),
    ]
