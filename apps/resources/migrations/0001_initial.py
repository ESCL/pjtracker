# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('accounts', '0001_initial'),
        ('work', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentTypeLabourType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType')),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(blank=True, null=True, to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='resources.Resource', primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('gender', models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])),
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
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='resources.Resource', primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=128, help_text='Manufacturer brand and model.')),
                ('year', models.PositiveIntegerField(help_text='Year of manufacture.')),
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
            field=models.ForeignKey(null=True, to='work.Project'),
        ),
        migrations.AddField(
            model_name='resource',
            name='team',
            field=models.ForeignKey(null=True, to='organizations.Team'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='labour_types',
            field=models.ManyToManyField(through='resources.EquipmentTypeLabourType', to='work.LabourType'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='parent',
            field=models.ForeignKey(related_name='subtypes', null=True, to='resources.EquipmentType'),
        ),
        migrations.AddField(
            model_name='positionhistory',
            name='employee',
            field=models.ForeignKey(to='resources.Employee'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(to='resources.EquipmentType'),
        ),
    ]
