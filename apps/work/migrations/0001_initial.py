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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabourType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=2)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=32)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
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
            field=models.ForeignKey(to='accounts.Account', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='parent',
            field=models.ForeignKey(to='work.Activity', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(to='work.Project'),
        ),
    ]
