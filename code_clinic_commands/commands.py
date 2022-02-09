"""
Commands for the WTC Code Clinic Booking System.

"""
from google.auth import credentials

import code_clinic_api
import code_clinic_calendar_files
import code_clinic_config
from code_clinic_authentication import code_clinic_token
from code_clinic_io import code_clinic_output


def login():
    user_name = code_clinic_config.get_username()
    user_token = code_clinic_token.get_user_token(user_name)
    code_clinic_token.get_clinic_token()
    code_clinic_output.login_results()
    return user_token


def help_command():
    """
    Contains a list of valid commands.
    """
    code_clinic_output.display_help()


def update_local_calendar(
        token_credentials: credentials.Credentials,
        file_name: str) -> None:
    """
    Updates the specified calendar file with the Google Calendar data
    :param credentials.Credentials token_credentials: Token credentials
    :param str file_name: Reference to the specified calendar file
    :return: None
    """
    calendar_data: dict[str, list[dict]] = \
        code_clinic_api.get_formated_calendar_events(token_credentials)

    if file_name == 'user':
        code_clinic_calendar_files.update_user_calendar_file(calendar_data)
    elif file_name == 'clinic':
        code_clinic_calendar_files.update_clinic_calendar_file(calendar_data)


def display_calendar(
        token_credentials: credentials.Credentials,
        file_name: str) -> None:
    """
    Command to display the Google Calendar events
    :param credentials.Credentials token_credentials:Token credentials
    :param str file_name: Reference to the specified calendar file
    :return: None
    """
    update_local_calendar(token_credentials, file_name)
    calendar_events: dict[str, list[dict]] = {}

    if file_name == 'user':
        calendar_events = code_clinic_calendar_files.read_user_calendar_file()
    elif file_name == 'clinic':
        calendar_events = code_clinic_calendar_files.read_clinic_calendar_file()

    code_clinic_output.output_calendar(calendar_events)


def display_volunteer_slots(clinic_credentials: credentials.Credentials):
    """

    :param clinic_credentials:
    :return:
    """
    update_local_calendar(clinic_credentials, 'clinic')

    clinic_calendar_event_data: dict[str, list[dict]] = \
        code_clinic_calendar_files.read_clinic_calendar_file()

    code_clinic_output.output_volunteer_slots(clinic_calendar_event_data)


def command_handler(command_arg):
    """It handles commands from the command line arguments.
    """
    if command_arg in {'-h', 'help', '--help', ''}:
        help_command()
        return
    elif command_arg == 'login':
        login()
        return
    elif code_clinic_token.check_user_token_expired():
        code_clinic_output.output_token_expired()
        return

    user_credentials: credentials.Credentials = \
        code_clinic_token.return_user_token_creds()

    clinic_credentials: credentials.Credentials = \
        code_clinic_token.return_clinic_credentials()

    if command_arg == 'student_calendar':
        display_calendar(user_credentials, 'user')
    elif command_arg == 'clinic_calendar':
        display_calendar(clinic_credentials, 'clinic')
    elif command_arg == 'volunteer_slots':
        display_volunteer_slots(clinic_credentials)
