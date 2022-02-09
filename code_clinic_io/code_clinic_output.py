"""
Output functions for Code Clinic Booking System

"""

import helpers
import tabulate

def welcome_msg():
    """It displays a welcome message to the user.
    """

    print("Welcome to WeThinkCode's Code Clinic Booking System.")


def login_results():
    """
    Function displays the login results, when a user attempts to login.
    """

    print('Login successful')


def display_help():
    """
    It displays the range of commands to the user, when a user
    """

    print("""Here is a list of valid commands:
> login - Enables the user to login to the system
> student_calendar - Allows the user to view their student calendar
> clinic_calendar - Allows the user to view the code clinic calendar 
""")


def login_prompt(username):

    print(f'{username}: Please login')


def output_token_expired() -> None:
    """
    Prints out a token expiration message for the user
    :return: None
    """
    print('\nToken expired.\n\nPlease login using\n\n    code-clinic login\n')


def output_no_events_found() -> None:
    """
    Prints out a no calendar events found message
    :return: None
    """
    print('There are currently no upcoming events.')


def output_calendar(calendar_event_data: dict[str, list[dict]]) -> None:
    """
    Prints out calendar events to the user in the form of a table
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    if not calendar_event_data:
        output_no_events_found()
        return

    output_table: list[list[str, str, str]] = \
        helpers.format_calendar_events_to_table(calendar_event_data)

    print(
        tabulate.tabulate(
            output_table,
            headers=['Date', 'Time', 'Event Summary'],
            tablefmt='fancy_grid')
    )


def output_volunteer_slots(clinic_calendar_event_data: dict[str, list[dict]]) \
        -> None:
    """
    Prints out the clinic calendar time slots in the form of a table
    :param dict[str, list[dict]] clinic_calendar_event_data: Clinic calendar
    event data
    :return: None
    """
    output_table: list[list[str, str, str]] = \
        helpers.format_clinic_time_slots_to_table(clinic_calendar_event_data)

    headers: list[str, ...] = ['Date\\Time',
                               '09:00AM', '09:30AM',
                               '10:00AM', '10:30AM',
                               '11:00AM', '11:30PM',
                               '12:00PM', '12:30PM',
                               '13:00PM', '13:30PM',
                               '14:00PM', '14:30PM',
                               '15:00PM', '15:30PM',
                               '16:00PM', '16:30PM',
                               '17:00PM', '17:30PM']

    print(
        tabulate.tabulate(
            output_table,
            headers=headers,
            stralign='center',
            tablefmt='fancy_grid')
    )
