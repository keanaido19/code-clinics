import unittest
from io import StringIO
import sys
from unittest.mock import patch
import datetime
import helpers
import re


class test_helpers_function(unittest.TestCase):

    def test_get_current_utc_date(self):
        date_1 = helpers.get_current_utc_date()
        self.assertLessEqual(date_1, datetime.datetime.utcnow())

    def test_get_new_utc_date(self):
        days = 7
        new_date = helpers.get_current_utc_date().date() + datetime.timedelta(days=days + 1)
        new_time = datetime.datetime.min.time()
        self.assertEqual(helpers.get_new_utc_date(days), datetime.datetime.combine(new_date, new_time))
    
    def test_verify_email_address(self):
        email_1 = "syd@yahoo.com"
        email_2 = "syd464@hotmail.com"
        email_3 = "noksitho021@student.wethinkcode.co.za"
        self.assertFalse(helpers.verify_email_address(email_1), re.match(r'^\w+@student.wethinkcode.co.za$', email_1) and  \
        not not helpers.validate_email.validate_email(email_1, verify=True))

        self.assertFalse(helpers.verify_email_address(email_2),re.match(r'^\w+@student.wethinkcode.co.za$', email_2) and  \
        not not helpers.validate_email.validate_email(email_2, verify=True))

        self.assertTrue(helpers.verify_email_address(email_3), re.match(r'^\w+@student.wethinkcode.co.za$', email_3) and  \
        not not helpers.validate_email.validate_email(email_3, verify=True))

    @patch("sys.stdin", StringIO("DBN\n"))
    def test_get_campus_location_correct_campus(self):
        campus_location = helpers.code_clinic_input.get_location()
        self.assertEqual(helpers.verify_campus_location(campus_location),True)

    @patch("sys.stdin", StringIO("NY\n"))
    def test_get_campus_location_wrong_campus(self):
        campus_location = helpers.code_clinic_input.get_location()
        self.assertEqual(helpers.verify_campus_location(campus_location), False)










if __name__ == '__main__':
    unittest.main()