# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('resources', '0001_initial'), ('resources', '0002_auto_20160326_1616')]

    dependencies = [
        ('work', '__first__'),
        ('accounts', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
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
                ('owner', models.ForeignKey(blank=True, to='accounts.Account', null=True)),
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
            name='Employee',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, to='resources.Resource', serialize=False, parent_link=True, primary_key=True)),
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
                ('resource_ptr', models.OneToOneField(auto_created=True, to='resources.Resource', serialize=False, parent_link=True, primary_key=True)),
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
            field=models.ForeignKey(blank=True, to='accounts.Account', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='project',
            field=models.ForeignKey(blank=True, to='work.Project', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='team',
            field=models.ForeignKey(blank=True, to='organizations.Team', null=True),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='labour_types',
            field=models.ManyToManyField(through='resources.EquipmentTypeLabourType', to='work.LabourType'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='owner',
            field=models.ForeignKey(blank=True, to='accounts.Account', null=True),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='parent',
            field=models.ForeignKey(to='resources.EquipmentType', related_name='subtypes', null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(to='resources.EquipmentType'),
        ),
        migrations.AddField(
            model_name='equipmenttype',
            name='code',
            field=models.CharField(max_length=4, default='LOL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmenttype',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
