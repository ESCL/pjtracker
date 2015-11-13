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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentTypeLabourType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_type', models.ForeignKey(to='resources.EquipmentType')),
                ('labour_type', models.ForeignKey(to='work.LabourType')),
                ('owner', models.ForeignKey(to='accounts.Account', blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('resource_ptr', models.OneToOneField(primary_key=True, to='resources.Resource', auto_created=True, serialize=False, parent_link=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('photo', models.FileField(upload_to='', max_length=256, blank=True)),
                ('home_address', models.CharField(null=True, max_length=256, blank=True)),
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
                ('resource_ptr', models.OneToOneField(primary_key=True, to='resources.Resource', auto_created=True, serialize=False, parent_link=True)),
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
            field=models.ForeignKey(to='accounts.Account', blank=True, null=True),
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
            model_name='equipmenttype',
            name='labour_types',
            field=models.ManyToManyField(through='resources.EquipmentTypeLabourType', to='work.LabourType'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='owner',
            field=models.ForeignKey(to='accounts.Account', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='parent',
            field=models.ForeignKey(to='resources.EquipmentType', related_name='subtypes', null=True),
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
