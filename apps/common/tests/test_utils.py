__author__ = 'kako'

from django.test import TestCase

from ..utils import generate_code_from_name


class UtilsTest(TestCase):

    def test_generate_code_from_name(self):
        # Two words, len 2-3 > initials
        res = generate_code_from_name('Planning Engineer', min_len=2, max_len=3)
        self.assertEqual(res, 'PE')

        # Two words, len 3 > two from first word, initial from second
        res = generate_code_from_name('Planning Engineer', min_len=3, max_len=3)
        self.assertEqual(res, 'PLE')

        # Three words, len 2 > first two initials
        res = generate_code_from_name('Planning Engineer Junior', min_len=2, max_len=2)
        self.assertEqual(res, 'PE')

        # Three words, len 2-4 > all initials
        res = generate_code_from_name('Planning Engineer Junior', min_len=2, max_len=4)
        self.assertEqual(res, 'PEJ')

        # Three words, len 4 > two from first word, other intials
        res = generate_code_from_name('Planning Engineer Junior', min_len=4, max_len=4)
        self.assertEqual(res, 'PLEJ')

        # Check removal of "and" and "I"
        res = generate_code_from_name('Electrical And Instrumentation Engineer To The III', min_len=4, max_len=4)
        self.assertEqual(res, 'ELIE')
