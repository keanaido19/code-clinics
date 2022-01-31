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