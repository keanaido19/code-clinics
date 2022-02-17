import unittest
import code_clinic_config
from unittest.mock import patch
import json


class ConfigTestCase(unittest.TestCase):

    def test_update_config(self):
        email = 'test@student.wethinkcode.co.za'
        location = 'DBN'
        days = 7
        code_clinic_config.update_config(email, location, days)
        with open(code_clinic_config.get_path_to_config_file(), 'r') as f:
            config = json.load(f)
            self.assertEqual(config, {
                             "username": "test@student.wethinkcode.co.za", "campus": "DBN", "days": 7})

    def test_create_empty_config(self):
        code_clinic_config.delete_config_file()
        code_clinic_config.create_empty_config_file()
        with open(code_clinic_config.get_path_to_config_file(), 'r') as empty_config:
            config_data = empty_config.read()
            self.assertEqual(config_data, '')

    def test_get_username(self):
        email = 'test@student.wethinkcode.co.za'
        location = 'DBN'
        days = 7
        code_clinic_config.create_empty_config_file()
        code_clinic_config.update_config(email, location, days)
        username = code_clinic_config.get_username()
        self.assertEqual('test@student.wethinkcode.co.za', username)

    def test_get_campus_location(self):
        email = 'test@student.wethinkcode.co.za'
        location = 'DBN'
        days = 7
        code_clinic_config.create_empty_config_file()
        code_clinic_config.update_config(email, location, days)
        campus_location = code_clinic_config.get_campus_location()
        self.assertEqual('DBN', campus_location)

    def test_verify_config_false(self):
        email = 'test@gmail.com'
        location = 'BFM'
        days = 7
        code_clinic_config.create_empty_config_file()
        code_clinic_config.update_config(email, location, days)

        self.assertFalse(code_clinic_config.verify_config_file())

    def test_verify_config_true(self):
        email = 'danmulop021@student.wethinkcode.co.za'
        location = 'DBN'
        days = 7
        code_clinic_config.create_empty_config_file()
        code_clinic_config.update_config(email, location, days)
        self.assertTrue(code_clinic_config.verify_config_file())


if __name__ == '__main__':
    unittest.main()
