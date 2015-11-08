__author__ = 'kako'

from django.core.management.base import BaseCommand

from ....work.factories import ActivityGroupFactory, ActivityGroupTypeFactory


class Command(BaseCommand):
    """
    Create the standard activity groups for phases and disciplines for
    construction projects.
    """
    def handle(self, **options):
        # Setup generic activity groups
        print('Setting up activity groups...')
        groups = []

        # Create standard phases
        ph = ActivityGroupTypeFactory.create(name='Phase')
        groups.append(ActivityGroupFactory.create(name='Engineering', code='ENG', type=ph))
        groups.append(ActivityGroupFactory.create(name='Procurement', code='PRT', type=ph))
        groups.append(ActivityGroupFactory.create(name='Construction', code='CST', type=ph))
        groups.append(ActivityGroupFactory.create(name='Commissioning', code='COM', type=ph))

        # Create standard disciplines
        ds = ActivityGroupTypeFactory.create(name='Discipline')
        groups.append(ActivityGroupFactory.create(name='Civil', code='CIV', type=ds))
        groups.append(ActivityGroupFactory.create(name='Structural', code='STR', type=ds))
        groups.append(ActivityGroupFactory.create(name='Mechanical', code='MEC', type=ds))
        groups.append(ActivityGroupFactory.create(name='Piping', code='PIP', type=ds))
        groups.append(ActivityGroupFactory.create(name='Instrumentation', code='INS', type=ds))
        groups.append(ActivityGroupFactory.create(name='Pipelines', code='PPL', type=ds))

        print('Created activity groups: {}'.format(groups))
