"""
Output functions for Code Clinic Booking System

"""

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
> volunteer_calendar - Allows the user to view the code clinic calendar 
""")


def login_prompt(username):

    print(f'{username}: Please login')


def output_token_expired() -> None:
    """
    Prints out a token expiration message for the user
    :return: None
    """
    print('\nToken expired.\n\nPlease login using\n\n    code-clinic login\n')
