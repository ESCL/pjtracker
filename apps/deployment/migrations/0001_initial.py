# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.common.signals
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('work', '__first__'),
        ('organizations', '__first__'),
        ('resources', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=1, default='P')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('comments', models.CharField(null=True, max_length=256, blank=True)),
                ('owner', models.ForeignKey(to='accounts.Account', null=True, blank=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('action', models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=16)),
                ('feedback', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to='accounts.Account', null=True, blank=True)),
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
                ('account', models.OneToOneField(to='accounts.Account', related_name='timesheet_settings')),
                ('owner', models.ForeignKey(to='accounts.Account', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('labour_type', models.CharField(choices=[('M', 'Managerial'), ('I', 'Indirect'), ('D', 'Direct')], max_length=1)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('activity', models.ForeignKey(to='work.Activity', null=True, blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType', null=True)),
                ('owner', models.ForeignKey(to='accounts.Account', null=True, blank=True)),
                ('position', models.ForeignKey(to='organizations.Position', null=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(to='deployment.TimeSheet', related_name='work_logs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
