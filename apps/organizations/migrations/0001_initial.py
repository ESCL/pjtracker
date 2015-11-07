# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('work', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('managerial_labour', models.BooleanField(default=False)),
                ('indirect_labour', models.BooleanField(default=False)),
                ('direct_labour', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(unique=True, max_length=16)),
                ('activities', models.ManyToManyField(blank=True, to='work.Activity')),
                ('company', models.ForeignKey(to='organizations.Company')),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
                ('supervisors', models.ManyToManyField(blank=True, related_name='supervised_teams', to=settings.AUTH_USER_MODEL)),
                ('timekeepers', models.ManyToManyField(blank=True, related_name='timekept_teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
