import unittest
from io import StringIO
import sys
from unittest.mock import patch
import datetime
import os
import code_clinic_calendar_files as clf
import re


class test_calendar_files_function(unittest.TestCase):

    def test_get_path_to_calendar(self):

        self.assertEqual(clf.get_path_to_calendar_file_directory(), os.path.join(os.environ["HOME"], '.local/code_clinic/calendar_files'))

    


    













if __name__ == '__main__':
    unittest.main()