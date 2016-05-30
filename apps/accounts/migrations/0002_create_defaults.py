from django.contrib.auth.hashers import make_password
from django.db import migrations

from ..utils import ensure_permissions


def bootstrap_default_groups(apps, schema_editor):
    """
    Add default groups with their corresponding permissions.
    """
    # Get models
    # Note: We can't import the models directly as they may be a newer
    # version than this migration expects
    User = apps.get_model('accounts', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    TimeSheet = apps.get_model('deployment', 'TimeSheet')
    TimeSheetSettings = apps.get_model('deployment', 'TimeSheetSettings')
    Company = apps.get_model('organizations', 'Company')
    Team = apps.get_model('organizations', 'Team')
    Position = apps.get_model('organizations', 'Position')
    CalendarDay = apps.get_model('payroll', 'CalendarDay')
    HourType = apps.get_model('payroll', 'HourType')
    Period = apps.get_model('payroll', 'Period')
    WorkedHours = apps.get_model('payroll', 'WorkedHours')
    Employee = apps.get_model('resources', 'Employee')
    Equipment = apps.get_model('resources', 'Equipment')
    EquipmentType = apps.get_model('resources', 'EquipmentType')
    Activity = apps.get_model('work', 'Activity')
    ActivityGroup = apps.get_model('work', 'ActivityGroup')
    ActivityGroupType = apps.get_model('work', 'ActivityGroupType')
    LabourType = apps.get_model('work', 'LabourType')
    Project = apps.get_model('work', 'Project')

    # Admin group
    # Note: timesheet settings perm also gives perm to hour type range and
    # standard hours, since their form is in the same view
    name = 'Administrators'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(User, ['change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(TimeSheetSettings, ['change'],
                                              permission_model=Permission))

    # HR group
    name = 'Human Resources'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(Company, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Position, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Employee, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(CalendarDay, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(HourType, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Period, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(WorkedHours, ['add'],
                                              permission_model=Permission))

    # Team management
    name = 'Team Management'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(Team, ['add', 'change'],
                                              permission_model=Permission))

    # PCON group
    name = 'Project Control'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(Team,  ['change activities'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Position, ['change labour types'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Equipment, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(EquipmentType, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Project, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(Activity, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(ActivityGroup, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(ActivityGroupType, ['add', 'change'],
                                              permission_model=Permission))
    group.permissions.add(*ensure_permissions(LabourType, ['add', 'change'],
                                              permission_model=Permission))

    # Timekeeping group
    name = 'Time-Keeping'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(TimeSheet, ['add', 'change', 'issue'],
                                              permission_model=Permission))

    # Supervision group
    name = 'Supervision'
    group = Group.objects.get_or_create(name=name)[0]
    group.permissions.add(*ensure_permissions(TimeSheet, ['review'],
                                              permission_model=Permission))


def create_superuser(apps, schema_editor):
    """
    Add standard superuser.
    """
    # Get models
    # Note: We can't import the models directly as they may be a newer
    # version than this migration expects
    User = apps.get_model('accounts', 'User')

    # Create superuser
    User.objects.get_or_create(
        username='root',
        password=make_password('123'),
        is_superuser=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('deployment', '0001_initial'),
        ('notifications', '0001_initial'),
        ('organizations', '0001_initial'),
        ('payroll', '0001_initial'),
        ('resources', '0001_initial'),
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(bootstrap_default_groups),
        migrations.RunPython(create_superuser)
    ]
