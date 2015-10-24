# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='location',
        ),
        migrations.AlterField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='parent',
            field=models.ForeignKey(blank=True, related_name='sub_activities', null=True, to='work.Activity'),
        ),
        migrations.AlterField(
            model_name='activitygroup',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='activitygrouptype',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to='accounts.Account'),
        ),
    ]
