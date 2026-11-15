from django.test import TestCase

from appuser.utils import validate_password_strength


class PasswordUtilTest(TestCase):
    def test_password_length(self):
        test_password = 'b@naN3s'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue('Password must be at least 9 characters' in errors)

    def test_password_contains_upper(self):
        test_password = 'b@nan3s123'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue(
            'Password must contain at least one uppercase letter' in errors
        )

    def test_password_contains_lower(self):
        test_password = 'B@NAN3S%^&'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue(
            'Password must contain at least one lowercase letter' in errors
        )

    def test_password_contains_number(self):
        test_password = 'B@NAnaS%^&'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue(
            'Password must contain at least one number' in errors
        )

    def test_password_contains_special(self):
        test_password = 'BANAnaS123'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue(
            'Password must contain at least one special character' in errors
        )

    def test_password_contains_no_spaces(self):
        test_password = 'BAnaN@ S123'
        is_valid, errors = validate_password_strength(test_password)
        self.assertFalse(is_valid)
        self.assertTrue(
            'Password cannot have spaces' in errors
        )

    def test_password_meets_requirements(self):
        test_password = 'BAnaN@S123'
        is_valid, errors = validate_password_strength(test_password)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
