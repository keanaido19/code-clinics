import unittest
from test_base import captured_output
from code_clinic_io.code_clinic_output import *


class TestOutputs(unittest.TestCase):
    def test_welcome_msg(self):
        with captured_output() as (out, err):
            welcome_msg()
        output = out.getvalue().strip()
        self.assertEqual(output, "Welcome to WTC Code Clinic Booking System\nYou do not appear to "
                         "have a config file defined...")


    def test_output_login_prompt(self):
        with captured_output() as (out, err):
            username = 'noksitho021@student.wethinkcode.co.za'
            output_login_prompt(username)
        output = out.getvalue().strip()
        self.assertIs(type(username), str)

    def test_output_token_expired(self):
        with captured_output() as (out, err):
            output_token_expired()
        output = out.getvalue().strip()
        self.assertEqual(
            output, 'Token expired.\n\nPlease login using\n\n    code-clinic login')

    def test_booking_successful(self):
        with captured_output() as (out, err):
            time_slot = '12'
            output_booking_successful(time_slot)
        output = out.getvalue().strip()
        self.assertEqual(
            output, 'Code Clinic time slot - 12 - successfully booked!')


if __name__ == '__main__':
    unittest.main()
