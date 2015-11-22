# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import apps.common.signals


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work', '__first__'),
        ('organizations', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(default='P', max_length=1, choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')])),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(blank=True, max_length=256, null=True)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.CharField(max_length=16, choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')])),
                ('feedback', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('timesheet', models.ForeignKey(related_name='actions', to='deployment.TimeSheet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeSheetSettings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('approval_policy', models.CharField(default='A', max_length=1, choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')])),
                ('rejection_policy', models.CharField(default='F', max_length=1, choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')])),
                ('account', models.OneToOneField(related_name='timesheet_settings', to='accounts.Account')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('activity', models.ForeignKey(null=True, to='work.Activity', blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType', null=True)),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('position', models.ForeignKey(to='organizations.Position', null=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(related_name='work_logs', to='deployment.TimeSheet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
