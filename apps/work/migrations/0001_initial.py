# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=32)),
                ('location', models.ForeignKey(to='geo.Location')),
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
            field=models.ManyToManyField(to='work.ActivityGroup'),
        ),
        migrations.AddField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(to='accounts.Account', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='parent',
            field=models.ForeignKey(related_name='sub_activities', to='work.Activity', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(to='work.Project'),
        ),
    ]
