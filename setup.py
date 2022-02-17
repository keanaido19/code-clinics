"""
Setup file to install the WTC Code Clinic Booking System
"""

from setuptools import setup

setup(
    name='code_clinics_group_project',
    version='1.0.0',
    packages=['code_clinic', 'code_clinic_io', 'code_clinic_tests',
              'code_clinic_commands', 'code_clinic_authentication'],
    py_modules=['code_clinic_api', 'code_clinic_calendar_export',
                'code_clinic_calendar_files', 'code_clinic_config', 'helpers','test_base', 'test_code_clinic_calendar_files','test_code_clinic_input','test_code_clinic_output', 'test_config','test_helpers'],
    url='https://gitlab.wethinkco.de/noksitho021/code_clinics_group_project',
    author='Team A Obliviate',
    author_email='danmulopo021@student.wethinkcode.co.za, '
                 'keanaido021@student.wethinkcode.co.za, '
                 'mzomdubeki021@student.wethinkcode.co.za, '
                 'noksitho021@student.wethinkcode.co.za',
    description='WTC Code Clinic Booking System',
    install_requires=["setuptools", "pytz", "py3dns", "validate_email",
                      "tabulate", "google-api-python-client",
                      "google-auth-httplib2", "google-auth-oauthlib",
                      "icalendar"],
    entry_points={"console_scripts": ["code-clinic = code_clinic.main:main"]},
)
