import unittest
from io import StringIO
from test_base import captured_io
from code_clinic_io.code_clinic_input import *

class TestInputs(unittest.TestCase):

    def test_get_location(self):
        with captured_io(StringIO('dbn\n')) as (out, err):
            get_location()
        
        output = out.getvalue().strip()
        self.assertEqual(output, 'Please enter your campus location (DBN\JHB\CPT):')

    def test_input_confirm_cancel_code_clinic_time_slot(self):
        with captured_io(StringIO('student\n12\n')) as (out, err):
            user_type = 'student'
            time_slot = '12'
            input_confirm_cancel_code_clinic_time_slot(time_slot, user_type)
        output = out.getvalue().strip()
        self.assertEqual(output, 'Confirm cancellation of student booking for Code '
                 'Clinic time slot : 12? (yes\\no)')

    def test_input_logout_prompt(self):
        with captured_io(StringIO('YES')) as (out, err):
            input_logout_prompt()

        output = out.getvalue().strip()
        self.assertEqual(output, 'Are you sure you want to log out? (yes/no)')

    def test_is_a_string(self):
        with captured_io(StringIO('noksitho021@student.wethinkcode.co.za')) as (out, err):
            get_username()
        output = out.getvalue().strip()
        self.assertEqual(output, 'Please provide the username(email address) for the booking system:')
        
    def test_input_time_slot(self):
        with captured_io(StringIO('student\n12\n')) as (out, err):
            user_type = 'student'
            time_slot = '12'
            input_confirm_time_slot(time_slot, user_type)
        output = out.getvalue().strip()
        self.assertEqual(output, 'Confirm student booking for Code Clinic time slot : 12? (yes\\no)')


if __name__ == '__main__':
    unittest.main()