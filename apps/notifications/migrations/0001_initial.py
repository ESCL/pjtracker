# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import apps.common.signals


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('event_target_id', models.PositiveIntegerField()),
                ('event_type', models.CharField(max_length=16)),
                ('title', models.CharField(max_length=128)),
                ('message_template', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('status', models.CharField(choices=[('E', 'Active'), ('D', 'Dismissed')], max_length=1, default='E')),
                ('event_target_model', models.ForeignKey(to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, apps.common.signals.SignalsMixin),
        ),
    ]
