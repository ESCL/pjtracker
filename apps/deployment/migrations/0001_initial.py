# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '__first__'),
        ('organizations', '__first__'),
        ('geo', '__first__'),
        ('accounts', '0001_initial'),
        ('work', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(null=True, blank=True, max_length=256)),
                ('issuer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account')),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('labour_type', models.CharField(choices=[('I', 'Indirect'), ('D', 'Direct'), ('M', 'Managerial')], max_length=1)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('activity', models.ForeignKey(null=True, to='work.Activity', blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('employee', models.ForeignKey(to='resources.Employee')),
                ('location', models.ForeignKey(to='geo.Location')),
                ('position', models.ForeignKey(to='resources.Position')),
                ('timesheet', models.ForeignKey(related_name='work_logs', to='deployment.TimeSheet')),
            ],
        ),
    ]
