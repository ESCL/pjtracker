# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django_signals_mixin.mixin


class Migration(migrations.Migration):

    replaces = [('notifications', '0001_initial'), ('notifications', '0002_auto_20151203_1259'), ('notifications', '0003_auto_20151205_1819')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('event_target_id', models.PositiveIntegerField()),
                ('event_type', models.CharField(max_length=16)),
                ('title', models.CharField(max_length=128)),
                ('message_template', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('status', models.CharField(choices=[('E', 'Active'), ('D', 'Dismissed'), ('X', 'Disabled')], default='E', max_length=1)),
                ('event_target_model', models.ForeignKey(to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('action_label', models.CharField(null=True, max_length=128)),
                ('action_url', models.CharField(null=True, max_length=256)),
            ],
            bases=(models.Model, django_signals_mixin.mixin.SignalsMixin),
        ),
    ]
