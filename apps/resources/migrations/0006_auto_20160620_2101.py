# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 21:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160618_1521'),
        ('work', '0003_auto_20160517_0222'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0005_auto_20160423_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceProjectAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('reviewed_timestamp', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], max_length=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments_created', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_assignments', to='work.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='resource',
            name='project',
        ),
        migrations.AddField(
            model_name='resourceprojectassignment',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_assignments', to='resources.Resource'),
        ),
        migrations.AddField(
            model_name='resourceprojectassignment',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments_reviewed', to=settings.AUTH_USER_MODEL),
        ),
    ]