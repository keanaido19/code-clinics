"""
Code Clinic Booking System
Team A-Obliviate

1. danmulopo021@student.wethinkcode.co.za (Danny Mulopo)
2. keanaido021@student.wethinkcode.co.za (Keaton Naidoo)
3. mzomdubeki021@student.wethinkcode.co.za (Mzokhulayo Mdubeki)
4. noksitho021@student.wethinkcode.co.za (Nokwanda Sithole)

"""

import code_clinic_config
from code_clinic_io import code_clinic_input, code_clinic_output
from code_clinic_commands import commands


def main():
    """Main function for the code clinic booking system

    """

    if not code_clinic_config.check_if_config_file_exists():
        code_clinic_output.welcome_msg()
        username = code_clinic_input.get_username()
        code_clinic_config.create_config_file()
        code_clinic_config.update_config(username)
        code_clinic_output.display_help()
    else:
        system_arguments = code_clinic_input.get_argument()
        commands.command_handler(system_arguments)


if __name__ == '__main__':
    main()
