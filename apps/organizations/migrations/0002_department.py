# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_defaults'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
