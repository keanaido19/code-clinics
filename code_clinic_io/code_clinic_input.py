"""
Input functions for Code Clinic Booking System.

"""
import sys


def get_argument():
    """
    Returns an argument from the command line.
    """
    return " ".join(sys.argv[1:])


def get_username():
    """Prompts the user for a username.
    """

    return \
        input('Please provide the username for the booking system:\n').strip()


def input_confirm_time_slot(time_slot: str, user_type: str) \
        -> bool:
    """
    Asks the user to confirm whether they want to book the specified time slot
    :param str time_slot: Specified time slot to book
    :param str user_type: Type of user, volunteer or student
    :return: Boolean value
    """
    return input(f'\nConfirm {user_type} booking for Code Clinic time slot : '
                 f'{time_slot}? (yes\\no)\n').lower().strip() in {'yes', 'y'}


def get_location():
    """
    Prompts the user to enter their campus location
    """

    return input(
        'Please enter your campus location (DBN\\JHB\\CPT):\n').upper().strip()


def input_confirm_cancel_code_clinic_time_slot(time_slot: str, user_type: str) \
        -> bool:
    """
    Asks the user to confirm whether they want to cancel their volunteer
    booking at the specified time slot
    :param str time_slot: Specified time slot to book
    :param str user_type: str user_type: Type of user, volunteer or student
    :return: Boolean value
    """
    return input(f'\nConfirm cancellation of {user_type} booking for Code '
                 f'Clinic time slot : {time_slot}? (yes\\no)\n')\
        .lower().strip() in {'yes', 'y'}


def input_logout_prompt():
    '''
    It prompts the user to specify whether or not they do want to logout.
    '''
    return input('\nAre you sure you want to log out? (yes/no)\n')\
               .lower().strip() in {'yes', 'y'}
