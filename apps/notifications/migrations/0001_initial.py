# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import apps.common.signals
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('event_target_id', models.PositiveIntegerField()),
                ('event_type', models.CharField(max_length=16)),
                ('title', models.CharField(max_length=128)),
                ('message_template', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('event_target_model', models.ForeignKey(to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, apps.common.signals.SignalsMixin),
        ),
    ]
