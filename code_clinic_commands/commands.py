"""
Commands for the WTC Code Clinic Booking System.

"""

def login():
    pass


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
    """Contains a list of valid commands.
    """

    return """Here is a list of valid commands:
> login - Enables the user to login to the system
> student_calendar - Allows the user to view their student calendar
> volunteer_calendar - Allows the user to view the code clinic calendar 
"""