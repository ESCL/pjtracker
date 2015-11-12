# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=3, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionLabourType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
                ('position', models.ForeignKey(to='organizations.Position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16, unique=True)),
                ('activities', models.ManyToManyField(blank=True, to='work.Activity')),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
                ('supervisors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='supervised_teams')),
                ('timekeepers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='timekept_teams')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='position',
            name='labour_types',
            field=models.ManyToManyField(through='organizations.PositionLabourType', to='work.LabourType'),
        ),
        migrations.AddField(
            model_name='position',
            name='owner',
            field=models.ForeignKey(blank=True, to='accounts.Account', null=True),
        ),
    ]
