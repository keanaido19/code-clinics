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
from code_clinic_io import code_clinic_input


def main():
    """
    Main function for the code clinic booking system
    """

    if not code_clinic_config.verify_config_file():
        code_clinic_token.delete_user_token()
        code_clinic_config.create_config_file()
    else:
        system_arguments = code_clinic_input.get_argument()
        commands.command_handler(system_arguments)


if __name__ == '__main__':
    main()
