# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import apps.common.signals
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '__first__'),
        ('resources', '__first__'),
        ('work', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountSettings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('approval_policy', models.CharField(max_length=1, choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], default='A')),
                ('rejection_policy', models.CharField(max_length=1, choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], default='F')),
                ('account', models.OneToOneField(to='accounts.Account', related_name='timesheet_settings')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(max_length=1, choices=[('P', 'Preparing'), ('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], default='P')),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('action', models.CharField(max_length=16, choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')])),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('timesheet', models.ForeignKey(related_name='actions', to='deployment.TimeSheet')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('labour_type', models.CharField(max_length=1, choices=[('M', 'Managerial'), ('I', 'Indirect'), ('D', 'Direct')])),
                ('hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('activity', models.ForeignKey(to='work.Activity', null=True, blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('equipment_type', models.ForeignKey(null=True, to='resources.EquipmentType')),
                ('position', models.ForeignKey(null=True, to='organizations.Position')),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('timesheet', models.ForeignKey(related_name='work_logs', to='deployment.TimeSheet')),
            ],
        ),
    ]
