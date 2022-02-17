"""
Code Clinic Booking System
Team A-Obliviate

1. danmulopo021@student.wethinkcode.co.za (Danny Mulopo)
2. keanaido021@student.wethinkcode.co.za (Keaton Naidoo)
3. mzomdubeki021@student.wethinkcode.co.za (Mzokhulayo Mdubeki)
4. noksitho021@student.wethinkcode.co.za (Nokwanda Sithole)

"""

import code_clinic_config
from code_clinic_authentication import code_clinic_token
from code_clinic_commands import commands
from code_clinic_io import code_clinic_input,code_clinic_output
import re


def validate_code_clinic_command(command):
    """It handles the validation of commands from the command line arguments.
    returns True if command is valid
    returns False if an invalid command was entered
    """
    if command in {'-h', 'help', '--help', ''}:
        return True
    elif command == 'login':
        return True
    elif command == 'logout':
        return True
    elif command == 'calendar':
        return True
    elif command == 'clinic_calendar':
        return True
    elif command == 'volunteer_slots':
        return True
    elif re.match(r'^book_volunteer_slot \d+$', command):
        return True
    elif command == 'volunteer_bookings':
        return True
    elif re.match(r'^cancel_volunteer_booking \d+$', command):
        return True
    elif command == 'student_slots':
        return True
    elif re.match(r'^book_student_slot \d+$', command):
        return True
    elif command == 'student_bookings':
        return True
    elif re.match(r'^cancel_student_booking \d+$', command):
        return True
    elif re.match(r'^set_calendar_size \d+$', command):
        return True
    return False
    

def main():
    """
    Main function for the code clinic booking system
    """

    if not code_clinic_config.verify_config_file():
        code_clinic_token.delete_user_token()
        code_clinic_config.create_config_file()
    else:
        system_arguments = code_clinic_input.get_argument()
        if validate_code_clinic_command(system_arguments):
            commands.command_handler(system_arguments)
        else:
            code_clinic_output.output_invalid_code_clinic_command(system_arguments)

if __name__ == '__main__':
    main()
