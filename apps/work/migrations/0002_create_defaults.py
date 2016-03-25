# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_default_labour_types(apps, schema_editor):
    """
    Create default labour types.
    """
    # Get models
    # Note: We can't import the models directly as they may be a newer
    # version than this migration expects
    LabourType = apps.get_model('work', 'LabourType')

    # Ensure types MG, IN and DI exist
    LabourType.objects.get_or_create(name='Management', code='MG')
    LabourType.objects.get_or_create(name='Indirect', code='IN')
    LabourType.objects.get_or_create(name='Direct', code='DI')


def create_default_activity_groups(apps, schema_editor):
    """
    Create default activity groups and their types.
    """
    # Get models
    # Note: We can't import the models directly as they may be a newer
    # version than this migration expects
    ActivityGroupType = apps.get_model('work', 'ActivityGroupType')
    ActivityGroup = apps.get_model('work', 'ActivityGroup')

    # Create group types phase and discipline
    phase = ActivityGroupType.objects.get_or_create(name='Phase')[0]
    discipline = ActivityGroupType.objects.get_or_create(name='Discipline')[0]

    # Create phase groups
    ActivityGroup.objects.get_or_create(type=phase, code='ENG', name='Engineering')
    ActivityGroup.objects.get_or_create(type=phase, code='PRT', name='Procurement')
    ActivityGroup.objects.get_or_create(type=phase, code='CST', name='Construction')
    ActivityGroup.objects.get_or_create(type=phase, code='COM', name='Commissioning')

    # Create discipline groups
    ActivityGroup.objects.get_or_create(type=discipline, code='CIV', name='Civil')
    ActivityGroup.objects.get_or_create(type=discipline, code='STR', name='Structural')
    ActivityGroup.objects.get_or_create(type=discipline, code='MEC', name='Mechanical')
    ActivityGroup.objects.get_or_create(type=discipline, code='PIP', name='Piping')
    ActivityGroup.objects.get_or_create(type=discipline, code='INS', name='Instrumentation')
    ActivityGroup.objects.get_or_create(type=discipline, code='PPL', name='Pipeline')


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_squashed_0002_auto_20160301_2035'),
    ]

    operations = [
        migrations.RunPython(create_default_labour_types),
        migrations.RunPython(create_default_activity_groups)
    ]
