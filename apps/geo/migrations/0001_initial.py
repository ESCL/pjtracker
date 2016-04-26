# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_defaults'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(max_digits=7, decimal_places=5, null=True, blank=True)),
                ('longitude', models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)),
                ('owner', models.ForeignKey(to='accounts.Account', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
