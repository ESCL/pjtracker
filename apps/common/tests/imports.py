__author__ = 'kako'

from csv import DictWriter
from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase

from ..test import mock
from ...accounts.factories import AccountFactory
from ...accounts.models import Account, User


class ImportTest(TestCase):

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
        account = AccountFactory.create()
        self.assertRaises(FileNotFoundError, call_command, 'import_data',
                          'Employee', 'employees.csv', account.code)

    @mock.patch('apps.common.management.commands.import_data.DictWriter.writerow', mock.MagicMock())
    @mock.patch('apps.common.management.commands.import_data.open', create=True)
    def test_import_user(self, open_mock):
        # stringio to capture command stdout
        stdout = StringIO()

        # Create an account to use for imports, make sure it has no users
        account = AccountFactory.create()
        self.assertEqual(User.objects.filter(owner=account).count(), 0)

        # Use a broken file
        i_file = StringIO('a,b,c,d\n1,2,3,4')
        i_file.name = 'users.csv'
        open_mock.return_value = i_file
        call_command('import_data', 'User', i_file.name, account.code, stdout=stdout)

        # Nothing created, 1 error found
        self.assertEqual(User.objects.filter(owner=account).count(), 0)
        self.assertIn('1 errors', stdout.getvalue())

        # Failed row was written to error file
        DictWriter.writerow.assert_called_once_with({'a': '1', 'b': '2', 'c': '3', 'd': '4'})
        DictWriter.writerow.reset_mock()

        # Use a correct file, with some broken data
        i_file = StringIO(
            'username,email,first_name,last_name,password\n'
            'pepe,pepe@lalal.com,,,p3p3\n'  # OK
            'rincewind,,Rince,Wind,r1nc3\n'  # OK
            ',,,,\n'  # error: missing everything
            ',mike@lalal.com,Mike,Litoris,m1k3\n'  # error: missing username
            'twoflower,,Twoflower,,\n'  # OK: password can be unset
        )
        i_file.name = 'users.csv'
        open_mock.return_value = i_file
        call_command('import_data', 'User', i_file.name, account.code, stdout=stdout)

        # Three users created, 2 errors found
        self.assertEqual(User.objects.filter(owner=account).count(), 3)
        self.assertIn('2 errors', stdout.getvalue())

        # Error file should be written twice: rows 3 and 4
        DictWriter.writerow.assert_has_calls([
            mock.call({'username': '', 'email': '', 'first_name': '',
                       'last_name': '', 'password': ''}),
            mock.call({'username': '', 'email': 'mike@lalal.com', 'first_name': 'Mike',
                       'last_name': 'Litoris', 'password': 'm1k3'})
        ])
