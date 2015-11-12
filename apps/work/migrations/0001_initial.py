# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=32)),
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
            field=models.ManyToManyField(to='work.ActivityGroup'),
        ),
        migrations.AddField(
            model_name='activity',
            name='labour_types',
            field=models.ManyToManyField(to='work.LabourType'),
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
    ]
