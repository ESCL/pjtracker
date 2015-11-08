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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('managerial_labour', models.BooleanField(default=False)),
                ('indirect_labour', models.BooleanField(default=False)),
                ('direct_labour', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(unique=True, max_length=16)),
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
    ]
