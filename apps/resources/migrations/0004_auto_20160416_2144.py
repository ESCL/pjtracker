# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_defaults'),
        ('resources', '0003_employee_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
                ('resource_type', models.CharField(max_length=32, choices=[('employee', 'Employees'), ('equipment', 'Equipment'), ('all', 'Both')])),
                ('owner', models.ForeignKey(null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='equipmenttype',
            name='parent',
            field=models.ForeignKey(null=True, to='resources.EquipmentType', blank=True, related_name='subtypes'),
        ),
        migrations.AddField(
            model_name='resource',
            name='category',
            field=models.ForeignKey(null=True, to='resources.ResourceCategory', blank=True),
        ),
    ]
