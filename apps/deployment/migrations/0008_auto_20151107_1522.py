# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('deployment', '0007_auto_20151107_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountSettings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('approval_policy', models.CharField(default='A', choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1)),
                ('rejection_policy', models.CharField(default='F', choices=[('F', 'Any'), ('M', 'Majority'), ('A', 'All')], max_length=1)),
                ('account', models.OneToOneField(to='accounts.Account')),
            ],
        ),
        migrations.AlterField(
            model_name='timesheetaction',
            name='action',
            field=models.CharField(choices=[('I', 'Issued'), ('R', 'Rejected'), ('A', 'Approved')], max_length=16),
        ),
    ]
