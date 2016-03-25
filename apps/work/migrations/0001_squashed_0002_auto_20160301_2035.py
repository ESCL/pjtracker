# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('work', '0001_initial'), ('work', '0002_auto_20160301_2035')]

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGroupType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabourType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=2)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activitygroup',
            name='type',
            field=models.ForeignKey(to='work.ActivityGroupType'),
        ),
        migrations.AddField(
            model_name='activity',
            name='groups',
            field=models.ManyToManyField(to='work.ActivityGroup', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='labour_types',
            field=models.ManyToManyField(to='work.LabourType', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='activity',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, to='work.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(to='work.Project'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='activitygroup',
            name='code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='activitygroup',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
