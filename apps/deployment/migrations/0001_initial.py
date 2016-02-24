# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django_signals_mixin


class Migration(migrations.Migration):

    dependencies = [
        ('work', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '__first__'),
        ('organizations', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1, default='P')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(blank=True, max_length=256, null=True)),
                ('owner', models.ForeignKey(null=True, blank=True, to='accounts.Account')),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, django_signals_mixin.SignalsMixin),
        ),
        migrations.CreateModel(
            name='TimeSheetAction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('action', models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=16)),
                ('feedback', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, blank=True, to='accounts.Account')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='actions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeSheetSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('approval_policy', models.CharField(choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1, default='A')),
                ('rejection_policy', models.CharField(choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1, default='F')),
                ('account', models.OneToOneField(related_name='timesheet_settings', to='accounts.Account')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('activity', models.ForeignKey(null=True, blank=True, to='work.Activity')),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType', null=True)),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(null=True, blank=True, to='accounts.Account')),
                ('position', models.ForeignKey(to='organizations.Position', null=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='work_logs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
