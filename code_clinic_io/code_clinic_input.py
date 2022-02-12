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

    username = input('Please enter username: ').strip()

    return username


def input_confirm_time_slot(time_slot: str, user_type: str) \
        -> bool:
    """
    Asks the user to confirm whether they want to book the specified time slot
    :param str time_slot: Specified time slot to book
    :param str user_type: Type of user, volunteer or student
    :return: Boolean value
    """
    return input(f'Confirm {user_type} booking for Code Clinic time slot : '
                 f'{time_slot}? (yes\\no)\n').lower().strip() in {'yes', 'y'}


def get_location():
    """
    Prompts the user to enter their campus location
    """

    return input(
        'Please enter your campus location (DBN\\JHB\\CPT): ').upper().strip()


def input_confirm_cancel_volunteer_slot(time_slot: str) \
        -> bool:
    """
    Asks the user to confirm whether they want to cancel their volunteer
    booking at the specified time slot
    :param str time_slot: Specified time slot to book
    :return: Boolean value
    """
    return input(f'Confirm cancellation of volunteer booking for Code Clinic '
                 f'time slot : {time_slot}? (yes\\no)\n').lower().strip() \
        in {'yes', 'y'}
