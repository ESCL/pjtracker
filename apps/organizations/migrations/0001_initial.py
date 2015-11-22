# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('work', '__first__'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(null=True, max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionLabourType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('position', models.ForeignKey(to='organizations.Position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=16)),
                ('activities', models.ManyToManyField(to='work.Activity', blank=True)),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
                ('supervisors', models.ManyToManyField(related_name='supervised_teams', blank=True, to=settings.AUTH_USER_MODEL)),
                ('timekeepers', models.ManyToManyField(related_name='timekept_teams', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='position',
            name='labour_types',
            field=models.ManyToManyField(to='work.LabourType', through='organizations.PositionLabourType'),
        ),
        migrations.AddField(
            model_name='position',
            name='owner',
            field=models.ForeignKey(null=True, to='accounts.Account', blank=True),
        ),
    ]
