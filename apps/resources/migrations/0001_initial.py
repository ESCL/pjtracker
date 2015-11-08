# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('organizations', '0001_initial'),
        ('work', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('team', models.ForeignKey(to='organizations.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('managerial_labour', models.BooleanField(default=False)),
                ('indirect_labour', models.BooleanField(default=False)),
                ('direct_labour', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
                ('parent', models.ForeignKey(null=True, related_name='subtypes', to='resources.EquipmentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('position', models.ForeignKey(to='organizations.Position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('team', models.ForeignKey(to='work.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(max_length=16)),
                ('resource_type', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('team', models.ForeignKey(to='organizations.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('resource_ptr', models.OneToOneField(serialize=False, auto_created=True, to='resources.Resource', primary_key=True, parent_link=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('photo', models.FileField(blank=True, max_length=256, upload_to='')),
                ('home_address', models.CharField(blank=True, max_length=256, null=True)),
                ('position', models.ForeignKey(to='organizations.Position')),
            ],
            options={
                'abstract': False,
            },
            bases=('resources.resource',),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('resource_ptr', models.OneToOneField(serialize=False, auto_created=True, to='resources.Resource', primary_key=True, parent_link=True)),
                ('type', models.ForeignKey(to='resources.EquipmentType')),
            ],
            options={
                'verbose_name_plural': 'equipment',
            },
            bases=('resources.resource',),
        ),
        migrations.AddField(
            model_name='resource',
            name='company',
            field=models.ForeignKey(to='organizations.Company'),
        ),
        migrations.AddField(
            model_name='resource',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='resource',
            name='project',
            field=models.ForeignKey(to='work.Project'),
        ),
        migrations.AddField(
            model_name='resource',
            name='team',
            field=models.ForeignKey(to='organizations.Team'),
        ),
        migrations.AddField(
            model_name='positionhistory',
            name='employee',
            field=models.ForeignKey(to='resources.Employee'),
        ),
    ]
