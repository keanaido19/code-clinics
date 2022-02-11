"""
Commands for the WTC Code Clinic Booking System.

"""
import re

from google.auth import credentials

import code_clinic_api
import code_clinic_calendar_files
import code_clinic_config
import helpers
from code_clinic_authentication import code_clinic_token
from code_clinic_io import code_clinic_output, code_clinic_input


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
        code_clinic_api.get_formatted_calendar_events(token_credentials)

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


def display_volunteer_slots(clinic_credentials: credentials.Credentials) \
        -> None:
    """
    Displays the Code Clinic time slots to the user
    :param credentials. Credentials clinic_credentials: Clinic token credentials
    :return: None
    """
    update_local_calendar(clinic_credentials, 'clinic')

    clinic_calendar_event_data: dict[str, list[dict]] = \
        code_clinic_calendar_files.read_clinic_calendar_file()

    code_clinic_output.output_volunteer_slots(clinic_calendar_event_data)


def get_command_argument(command_arg: str) -> str:
    """
    Returns the command argument for the WTC Code Clinic Booking System command
    :param str command_arg: WTC Code Clinic Booking System command
    :return: Command argument
    """
    return command_arg.split(' ')[-1]


def book_volunteer_slot(clinic_credentials: credentials.Credentials,
                        command_arg: str) -> None:
    """
    Command to allow the user to book a WTC Code Clinic Booking System time slot
    as a volunteer
    :param credentials. Credentials clinic_credentials: Clinic token credentials
    :param str command_arg: WTC Code Clinic Booking System command
    :return: None
    """
    # Updates local clinic calendar file if data is not up-to-date
    update_local_calendar(clinic_credentials, 'clinic')

    # Retrieves the volunteer time slot index from the command
    volunteer_slot_key: str = get_command_argument(command_arg)

    # Retrieves the clinic calendar event data from the local file
    clinic_calendar_event_data: dict[str, list[dict]] = \
        code_clinic_calendar_files.read_clinic_calendar_file()

    # Retrieves the available volunteer slots to book
    available_volunteer_slots: dict[str, dict[str, str]] = \
        helpers.get_available_volunteer_slots(clinic_calendar_event_data)

    # Checks if volunteer time slot index from command is valid
    if helpers.check_dictionary_key_is_valid(
            volunteer_slot_key, available_volunteer_slots):

        # Retrieves the available time slot using the volunteer time slot index
        volunteer_slot: dict[str, str] = \
            available_volunteer_slots[volunteer_slot_key]
    else:
        code_clinic_output.output_volunteer_booking_slot_invalid()
        return

    # Confirms with the user if they wish to book the desired time slot
    if code_clinic_input.input_confirm_time_slot(
            volunteer_slot['datetime'], 'volunteer'):

        # Uses the API function to book the time slot
        code_clinic_api.book_code_clinic_time_slot(
            clinic_credentials, volunteer_slot['event_id'], 'Volunteer')

        code_clinic_output.output_booking_successful(volunteer_slot['datetime'])


def display_student_slots(clinic_credentials: credentials.Credentials) -> None:
    """
    Command to allow the user to view the available WTC Code Clinic Booking
    System time slots that can be booked as a student
    :param credentials.Credentials clinic_credentials: Clinic token credentials
    :return: None
    """
    # Updates local clinic calendar file if data is not up-to-date
    update_local_calendar(clinic_credentials, 'clinic')

    # Retrieves the clinic calendar event data from the local file
    clinic_calendar_event_data: dict[str, list[dict]] = \
        code_clinic_calendar_files.read_clinic_calendar_file()

    # Retrieves the username from the config file
    username: str = code_clinic_config.get_username()

    # Outputs the available student slots as a table
    code_clinic_output.output_student_slots(
        username, clinic_calendar_event_data)


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
    elif re.match(r'^book_volunteer_slot \d+$', command_arg):
        book_volunteer_slot(clinic_credentials, command_arg)
    elif command_arg == 'student_slots':
        display_student_slots(clinic_credentials)
    elif command_arg == 'my_volunteer_slots':
        display_my_volunteer_slots(user_credentials)


def display_my_volunteer_slots(user_credentials):
    update_local_calendar(user_credentials, 'user')
    user_calendar_event_data = code_clinic_calendar_files.read_user_calendar_file()
    username = code_clinic_config.get_username()
    import helpers
    helpers.get_retractable_volunteer_slots(user_calendar_event_data, username)