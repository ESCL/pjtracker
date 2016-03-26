# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    replaces = [('payroll', '0001_initial'), ('payroll', '0002_auto_20160326_1616')]

    dependencies = [
        ('resources', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarDay',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=3, choices=[('PH', 'Public Holiday'), ('NH', 'National Holiday'), ('SH', 'State Holiday')], db_index=True)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=6)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourTypeRange',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('day_type', models.CharField(max_length=3, choices=[('WD', 'Weekday'), ('SAT', 'Saturday'), ('SUN', 'Sunday'), ('PH', 'Public Holiday'), ('NH', 'National Holiday'), ('SH', 'State Holiday')])),
                ('limit', models.DecimalField(max_digits=4, decimal_places=2, default=24)),
                ('hour_type', models.ForeignKey(to='payroll.HourType')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'ordering': ('day_type', 'limit'),
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('forecast_start_date', models.DateField()),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardHours',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('day_type', models.CharField(max_length=3, choices=[('WD', 'Weekday'), ('SAT', 'Saturday'), ('SUN', 'Sunday'), ('PH', 'Public Holiday'), ('NH', 'National Holiday'), ('SH', 'State Holiday')])),
                ('hours', models.DecimalField(max_digits=4, decimal_places=2)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkedHours',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('phase', models.CharField(max_length=1, choices=[('D', 'Adjustment'), ('A', 'Actual'), ('F', 'Forecast'), ('R', 'Retroactive')], db_index=True)),
                ('hours', models.DecimalField(max_digits=5, decimal_places=2)),
                ('employee', models.ForeignKey(to='resources.Employee')),
                ('hour_type', models.ForeignKey(to='payroll.HourType')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('period', models.ForeignKey(to='payroll.Period')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='standardhours',
            unique_together=set([('owner', 'day_type')]),
        ),
    ]
