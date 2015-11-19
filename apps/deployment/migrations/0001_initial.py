# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.common.signals
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('work', '__first__'),
        ('accounts', '0001_initial'),
        ('resources', '__first__'),
        ('organizations', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(default='P', choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(blank=True, null=True, max_length=256)),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.common.signals.SignalsMixin),
        ),
        migrations.CreateModel(
            name='TimeSheetAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('action', models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=16)),
                ('feedback', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='actions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeSheetSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('approval_policy', models.CharField(default='A', choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1)),
                ('rejection_policy', models.CharField(default='F', choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1)),
                ('account', models.OneToOneField(to='accounts.Account', related_name='timesheet_settings')),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('activity', models.ForeignKey(blank=True, to='work.Activity', null=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType', null=True)),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
                ('position', models.ForeignKey(to='organizations.Position', null=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='work_logs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
