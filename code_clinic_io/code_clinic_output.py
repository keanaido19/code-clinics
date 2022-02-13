"""
Output functions for Code Clinic Booking System

"""
from __future__ import annotations
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
> my_calendar - Allows the user to view their student calendar
> clinic_calendar - Allows the user to view the code clinic calendar 
> volunteer_slots - ...
> book_volunteer_slot <index> - ...
> my_volunteer_bookings - ...
> cancel_volunteer_booking <index> - ...
> student_slots - ...
> book_student_slot <index> - ...
> my_student_bookings - ...
> cancel_student_booking <index> - ...
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

    output_table: list[list[str]] = \
        helpers.format_calendar_events_to_table(calendar_event_data)

    print(
        tabulate.tabulate(
            output_table,
            headers=['Date', 'Time', 'Event Summary'],
            stralign='center',
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

    headers: list[str] = \
        ['Date\\Time', '09:00AM', '09:30AM', '10:00AM', '10:30AM',
         '11:00AM', '11:30AM', '12:00PM', '12:30PM', '13:00PM', '13:30PM',
         '14:00PM', '14:30PM', '15:00PM', '15:30PM', '16:00PM', '16:30PM',
         '17:00PM', '17:30PM']

    print(
        tabulate.tabulate(
            output_table,
            headers=headers,
            stralign='center',
            tablefmt='fancy_grid')
    )
    print("\nAn indexed volunteer slot can be booked by using"
          "\n\n    code-clinic book_volunteer_slot <index>\n")


def output_volunteer_booking_slot_invalid() -> None:
    """
    Prints out an invalid volunteer booking slot message for the user
    :return: None
    """
    print("\nThe time slot you wish to book as a volunteer is not available,"
          "\n\nplease refer to the available time slots using\n\n    "
          "code-clinic volunteer_slots\n")


def output_booking_successful(time_slot: str) -> None:
    """
    Prints out a booking successful message to the user
    :param str time_slot: Specified time slot to book
    :return: Boolean value
    """
    print(f'\nCode Clinic time slot - {time_slot} - successfully booked!\n')


def output_no_available_student_bookings() -> None:
    """
    Prints out a no available student bookings message to the user
    :return: None
    """
    print('\nThere are currently no Code Clinic time slots that you can book '
          'as a student.\n')


def output_student_booking_slot_invalid():
    """
    Prints out an invalid student booking slot message for the user
    :return: None
    """
    print("\nThe time slot you wish to book as a student is not available,\n\n"
          "please refer to the available time slots using"
          "\n\n    code-clinic student_slots\n")


def output_student_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) \
        -> None:
    """
    Prints out the available student booking slots as a table
    :param str username: Current user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    output_table: list[list[str]] = \
        helpers.format_calendar_events_to_available_student_bookings(
        username, calendar_event_data)

    if not output_table:
        output_no_available_student_bookings()
        return

    print(
        tabulate.tabulate(
            output_table,
            headers=['Index', 'Date', 'Time', 'Campus', 'Volunteer'],
            stralign='center',
            tablefmt='fancy_grid')
    )

    print("\nAn indexed student slot can be booked by using"
          "\n\n    code-clinic book_student_slot <index>\n")


def output_no_available_user_booked_volunteer_slots() -> None:
    """
    Prints out a no user booked volunteer bookings message to the user
    :return: None
    """
    print('\nThere are currently no Code Clinic time slots that you '
          'have booked as a volunteer.\n')


def output_user_booked_volunteer_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) -> None:
    """
    Prints out the user's booked volunteer slots as a table
    :param str username: The user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    output_table: list[list[str]] = \
        helpers.format_user_booked_volunteer_slots_to_table(
            calendar_event_data, username)

    if not output_table:
        output_no_available_user_booked_volunteer_slots()
        return

    print(
        tabulate.tabulate(
            output_table,
            headers=['Index', 'Date', 'Time', 'Student'],
            stralign='center',
            tablefmt='fancy_grid')
    )
    print("\nAn indexed volunteer booking can be canceled by using"
          "\n\n    code-clinic cancel_volunteer_booking <index>\n")


def output_cancel_volunteer_booking_slot_invalid() -> None:
    """
    Prints out an invalid cancel volunteer booking slot message for the user
    :return: None
    """
    print("\nThe time slot you wish to cancel as a volunteer has not been "
          "booked by you, or has been booked by a student,\n\nplease refer to "
          "your volunteer bookings using\n\n    code-clinic "
          "my_volunteer_bookings\n")


def output_cancel_student_booking_slot_invalid() -> None:
    """
    Prints out an invalid cancel student booking slot message for the user
    :return: None
    """
    print("\nThe time slot you wish to cancel as a student has not been "
          "booked by you,\n\nplease refer to your student bookings using"
          "\n\n    code-clinic my_student_bookings\n")


def output_cancel_booking_successful(time_slot: str, user_type: str) -> None:
    """
    Prints out a cancellation successful message to the user
    :param str time_slot: Specified time slot to cancel
    :param str user_type: str user_type: Type of user, volunteer or student
    :return: Boolean value
    """
    print(f'\nCode Clinic {user_type} booking for time slot - {time_slot} - '
          f'successfully cancelled!\n')


def output_no_available_user_booked_student_slots() -> None:
    """
    Prints out a no user booked student bookings message to the user
    :return: None
    """
    print('\nThere are currently no Code Clinic time slots that you '
          'have booked as a student.\n')


def output_user_booked_student_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) -> None:
    """
    Prints out the user's booked student slots as a table
    :param str username: The user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    output_table: list[list[str]] = \
        helpers.format_user_booked_student_slots_to_table(
            calendar_event_data, username)

    if not output_table:
        output_no_available_user_booked_student_slots()
        return

    print(
        tabulate.tabulate(
            output_table,
            headers=['Index', 'Date', 'Time', 'Campus', 'Volunteer'],
            stralign='center',
            tablefmt='fancy_grid')
    )
    print("\nAn indexed student booking can be canceled by using"
          "\n\n    code-clinic cancel_student_booking <index>\n")
