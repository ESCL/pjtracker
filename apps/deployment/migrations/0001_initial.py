# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.common.signals
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('work', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '__first__'),
        ('resources', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1, default='P')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(max_length=256, blank=True, null=True)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action', models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=16)),
                ('feedback', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
                ('timesheet', models.ForeignKey(related_name='actions', to='deployment.TimeSheet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeSheetSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('approval_policy', models.CharField(choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1, default='A')),
                ('rejection_policy', models.CharField(choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1, default='F')),
                ('account', models.OneToOneField(related_name='timesheet_settings', to='accounts.Account')),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('labour_type', models.CharField(choices=[('M', 'Managerial'), ('I', 'Indirect'), ('D', 'Direct')], max_length=1)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('activity', models.ForeignKey(to='work.Activity', blank=True, null=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType', null=True)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
                ('position', models.ForeignKey(to='organizations.Position', null=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(related_name='work_logs', to='deployment.TimeSheet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
