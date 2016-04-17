__author__ = 'kako'

from csv import DictWriter
from io import StringIO
from unittest import mock

from django.core.management import call_command, CommandError
from django.test import TestCase

from ...accounts.factories import AccountFakeFactory
from ...accounts.models import Account, User
from ...organizations.models import Company, Position
from ...resources.models import Employee, Equipment, EquipmentType
from ...work.models import Activity, Project


class ImportDataTest(TestCase):

    def setUp(self):
        # We need an account for any import check
        self.account = AccountFakeFactory.create()

    def test_error(self):
        # No arguments provided
        self.assertRaises(CommandError, call_command, 'import_data')

        # Only model provided
        self.assertRaises(CommandError, call_command, 'import_data',
                          'Employee')

        # Only model and file provided
        self.assertRaises(CommandError, call_command, 'import_data',
                          'Employee', 'employees.csv')

        # All provided, but owner does not exist
        self.assertRaises(Account.DoesNotExist, call_command, 'import_data',
                          'Employee', 'employees.csv', 'lala')

        # All provided, but file does not exist
        self.assertRaises(FileNotFoundError, call_command, 'import_data',
                          'Employee', 'employees.csv', self.account.code)

    @mock.patch('apps.common.management.commands.import_data.DictWriter.writerow', mock.MagicMock())
    @mock.patch('apps.common.management.commands.import_data.open', create=True)
    def test_import_users(self, open_mock):
        # Use a broken file
        i_file = StringIO('a,b,c,d\n1,2,3,4')
        i_file.name = 'users.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'User', i_file.name, self.account.code,
                     stdout=stdout)

        # Nothing created, 1 error found
        self.assertEqual(User.objects.filter(owner=self.account).count(), 0)
        self.assertIn('1 errors', stdout.getvalue())

        # Failed row was written to error file
        DictWriter.writerow.assert_called_once_with({
            'a': '1', 'b': '2', 'c': '3', 'd': '4',
            'error': 'username field cannot be blank'
        })
        DictWriter.writerow.reset_mock()

        # Use a correct file, with some broken data
        i_file = StringIO(
            'username,email,first_name,last_name,password\n'
            # OK
            'pepe,pepe@lalal.com,,,p3p3\n'
            # OK: email is not required
            'rincewind,,Rince,Wind,r1nc3\n'
            # error: password cannot be unset
            'twoflower,,Twoflower,,\n'
            # error: missing username
            ',mike@lalal.com,Mike,Litoris,m1k3\n'
        )
        i_file.name = 'users.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'User', i_file.name, self.account.code,
                     stdout=stdout)

        # Two users created, two errors found
        self.assertEqual(User.objects.filter(owner=self.account).count(), 2)
        self.assertIn('2 errors', stdout.getvalue())

        # Two rows written to error file
        expected_calls = [
            mock.call({'username': 'twoflower', 'email': '', 'first_name': 'Twoflower',
                       'last_name': '', 'password': '',
                       'error': 'password field cannot be blank'}),
            mock.call({'username': '', 'email': 'mike@lalal.com', 'first_name': 'Mike',
                       'last_name': 'Litoris', 'password': 'm1k3',
                       'error': 'username field cannot be blank'})
        ]
        self.assertEqual(DictWriter.writerow.mock_calls, expected_calls)
        DictWriter.writerow.reset_mock()

        # Simulate fix of error file
        i_file = StringIO(
            'username,email,first_name,last_name,password,error\n'
            # OK
            'twoflower,,Twoflower,,picturesque,password cannot be blank\n'
            # OK
            'mike.litoris,mike@lalal.com,Mike,Litoris,m1k3,username cannot be blank\n'
        )
        i_file.name = 'users.errors.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'User', i_file.name, self.account.code,
                     stdout=stdout)

        # Two more users created no errors
        self.assertEqual(User.objects.filter(owner=self.account).count(), 4)
        self.assertNotIn('process found', stdout.getvalue())

        # Two rows written to error file
        self.assertFalse(DictWriter.writerow.called)

    @mock.patch('apps.common.management.commands.import_data.DictWriter.writerow', mock.MagicMock())
    @mock.patch('apps.common.management.commands.import_data.open', create=True)
    def test_import_employees(self, open_mock):
        # Simulate somewhat heterogeneous file with a few errors
        i_file = StringIO(
            'identifier,first_name,last_name,gender,company__code,company__name,position__code,position__name,project__code,project__name\n'
            # OK: all complete
            'gps930442,Mike,Litoris,M,GPS,Global Pundits Society,PLE,Planning Engineer,KOL,Kingdom of Loathing\n'
            # OK: project matched by code
            'gps930443,Michelle,Wazoo,F,NAP,Napoleon Brothers,PLE,,KOL,\n'
            # OK: all matched by code, no names required
            'gps930445,Peter,Griffin,M,GPS,,PLE,,KOL,\n'
            # OK: project not required
            'gps930444,Andres,Iniaquella,M,TRU,Toys R-Us,SAL,Salesman,,\n'
            # error: missing identifier
            ',Mike,Litoris,M,GPS,Global Pundits Society,PLE,Planning Engineer,KOL,\n'
            # error: invalid gender
            'bon001,Jose,Bonaparte,Male,NAP,Napoleon Brothers,SAL,,,\n'
            # error: missing position code
            'lol123,Peter,Capusotto,M,GPS,,,Lala,,\n'
            # error: project name required to create it (code does not match)
            'lol124,Megatron,Griffin,F,GPS,,SAL,,TAT,\n'
        )
        i_file.name = 'users.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'Employee', i_file.name, self.account.code,
                     stdout=stdout)

        # Four employees created, 4 errors found
        self.assertEqual(Employee.objects.filter(owner=self.account).count(), 4)
        self.assertIn('4 errors', stdout.getvalue())

        # Check errors
        errors = [c[1][0].get('error') for c in DictWriter.writerow.mock_calls]
        self.assertEqual(errors, ['identifier field cannot be blank',
                                  'gender \'Male\' is not a valid choice',
                                  'code field cannot be blank',
                                  'name field cannot be blank'])

        # Check created companies: 3 (GPS, TRU, NAP)
        self.assertEqual(Company.objects.filter(owner=self.account).count(), 3)
        c1, c2, c3 = Company.objects.filter(owner=self.account).all()
        self.assertEqual(c1.name, 'Global Pundits Society')
        self.assertEqual(c2.name, 'Napoleon Brothers')
        self.assertEqual(c3.name, 'Toys R-Us')

        # Check created positions: 2 (PLE, SAL)
        self.assertEqual(Position.objects.filter(owner=self.account).count(), 2)
        p1, p2 = Position.objects.filter(owner=self.account).all()
        self.assertEqual(p1.name, 'Planning Engineer')
        self.assertEqual(p2.name, 'Salesman')

        # Check created projects: 1 (KOL)
        self.assertEqual(Project.objects.filter(owner=self.account).count(), 1)
        p1 = Project.objects.filter(owner=self.account).all()[0]
        self.assertEqual(p1.name, 'Kingdom of Loathing')

    @mock.patch('apps.common.management.commands.import_data.DictWriter.writerow', mock.MagicMock())
    @mock.patch('apps.common.management.commands.import_data.open', create=True)
    def test_import_equipment(self, open_mock):
        # Simulate somewhat heterogeneous file with a few errors
        i_file = StringIO(
            'identifier,model,year,company__code,company__name,type__code,type__name,project__code,project__name\n'
            # OK: all complete
            'mach001,Komatsu D340,1998,GPS,Global Pundits Society,EAR,Earthworks,KOL,Kingdom of Loathing\n'
            # OK: project matched by code
            'mach002,Caterpillar C1234,2006,NAP,Napoleon Brothers,LIF,Lifting,KOL,\n'
            # OK: all matched by code, project not required
            'mach003,American 4,2006,NAP,,LIF,,,\n'
            # error: missing identifier
            ',American 4,2006,NAP,,LIF,,,\n'
            # error: missing year
            'mach004,American 5,,NAP,,LIF,,,\n'
            # error: missing type code
            'mach003,American 6,2006,NAP,,,Sidebooms,,\n'
        )
        i_file.name = 'equipment.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'Equipment', i_file.name, self.account.code,
                     stdout=stdout)

        # Three equipment created, 2 errors found
        self.assertEqual(Equipment.objects.filter(owner=self.account).count(), 3)
        self.assertIn('3 errors', stdout.getvalue())

        # Check errors
        errors = [c[1][0].get('error') for c in DictWriter.writerow.mock_calls]
        self.assertEqual(errors, ['identifier field cannot be blank',
                                  'year field cannot be null',
                                  'code field cannot be blank'])

        # Check created companies: 2 (GPS, NAP)
        self.assertEqual(Company.objects.filter(owner=self.account).count(), 2)
        c1, c2 = Company.objects.filter(owner=self.account).all()
        self.assertEqual(c1.name, 'Global Pundits Society')
        self.assertEqual(c2.name, 'Napoleon Brothers')

        # Check created types: 2 (EAR, LIF)
        self.assertEqual(EquipmentType.objects.filter(owner=self.account).count(), 2)
        t1, t2 = EquipmentType.objects.filter(owner=self.account).all()
        self.assertEqual(t1.name, 'Earthworks')
        self.assertEqual(t2.name, 'Lifting')

        # Check created projects: 1 (KOL)
        self.assertEqual(Project.objects.filter(owner=self.account).count(), 1)
        p1 = Project.objects.filter(owner=self.account).all()[0]
        self.assertEqual(p1.name, 'Kingdom of Loathing')

    @mock.patch('apps.common.management.commands.import_data.DictWriter.writerow', mock.MagicMock())
    @mock.patch('apps.common.management.commands.import_data.open', create=True)
    def test_import_activities(self, open_mock):
        # Simulate somewhat heterogeneous file with a few errors
        i_file = StringIO(
            'full_wbs_code,name,project__code,project__name\n'
            # OK: all complete
            'X01.ENG,Engineering,X01,Some Project\n'
            # OK: project matched by code
            'X01.PRT,Procurement,X01,\n'
            # OK: project and parent matched by WBS code
            'X01.ENG.T01,Train 1,,\n'
            # OK: project and parent matched by WBS code
            'X01.ENG.T01.DES,Design,,\n'
            # error: w/o wbs we cannot determine parent
            ',Some activity,X02,Another Project\n'
            # error: missing name
            'X02.CST,,X02,Another Project\n'
            # error: bad wbs format
            'CST,Construction,X02,Another Project\n'
        )
        i_file.name = 'activities.csv'
        open_mock.return_value = i_file
        stdout = StringIO()
        call_command('import_data', 'Activity', i_file.name, self.account.code,
                     stdout=stdout)

        # Four activities created, 3 errors found
        self.assertEqual(Activity.objects.filter(owner=self.account).count(), 4)
        self.assertIn('3 errors', stdout.getvalue())

        # Check errors
        errors = [c[1][0].get('error') for c in DictWriter.writerow.mock_calls]
        self.assertEqual(errors, ['parent field cannot be blank',
                                  'name field cannot be blank',
                                  'WBS code format is invalid'])

        # Check created projects: 1 (X01)
        self.assertEqual(Project.objects.filter(owner=self.account).count(), 1)
        p1 = Project.objects.filter(owner=self.account).all()[0]
        self.assertEqual(p1.code, 'X01')
        self.assertEqual(p1.name, 'Some Project')

        # Check parents
        a1, a2, a3, a4 = Activity.objects.filter(owner=self.account).all()
        self.assertEqual(a1.code, 'ENG')
        self.assertEqual(a1.name, 'Engineering')
        self.assertEqual(a1.parent, None)
        self.assertEqual(a2.code, 'PRT')
        self.assertEqual(a2.name, 'Procurement')
        self.assertEqual(a2.parent, None)
        self.assertEqual(a3.code, 'T01')
        self.assertEqual(a3.name, 'Train 1')
        self.assertEqual(a3.parent, a1)
        self.assertEqual(a4.code, 'DES')
        self.assertEqual(a4.name, 'Design')
        self.assertEqual(a4.parent, a3)
