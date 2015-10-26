# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '__first__'),
        ('resources', '__first__'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work', '__first__'),
        ('organizations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=1, choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')])),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(blank=True, null=True, max_length=256)),
                ('issuer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('labour_type', models.CharField(max_length=1, choices=[('I', 'Indirect'), ('D', 'Direct'), ('M', 'Managerial')])),
                ('hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('activity', models.ForeignKey(null=True, to='work.Activity', blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('employee', models.ForeignKey(to='resources.Employee')),
                ('location', models.ForeignKey(to='geo.Location')),
                ('position', models.ForeignKey(to='organizations.Position')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='work_logs')),
            ],
        ),
    ]
