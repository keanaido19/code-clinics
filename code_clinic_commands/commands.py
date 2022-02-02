"""
Commands for the WTC Code Clinic Booking System.

"""
from code_clinic_io import code_clinic_output
import code_clinic_config
from code_clinic_authentication import code_clinic_token


def login():
    user_name = code_clinic_config.get_username()
    code_clinic_token.get_user_token(user_name)


def command_handler(command_arg):
    """It handles commands from the command line arguments.
    """
    if command_arg == 'login':
        login()
    elif command_arg == 'student_calendar':
        pass
    elif command_arg == 'clinic_calendar':
        pass


def help_command():
    """
    Contains a list of valid commands.
    """
    code_clinic_output.display_help()
