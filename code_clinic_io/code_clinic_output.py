"""
Output functions for Code Clinic Booking System

"""
import code_clinic_commands.commands as comm

def welcome_msg():
    """It displays a welcome message to the user.
    """

    print("Welcome to WeThinkCode's Code Clinic Booking System.")


def login_results():
    """
    Function displays the login results, when a user attempts to login.
    """

    print('Login successfull')


def display_help():
    """It displays the range of commands to the user
    """
    
    comm.help_command()
    
