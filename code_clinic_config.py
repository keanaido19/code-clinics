"""
Creates a config file.

"""
import os.path
import json
import helpers
from code_clinic_io import code_clinic_input, code_clinic_output

def create_config_directory():
    """
    Creates config directory
    """

    os.makedirs(get_path_to_clinic_directory())


def get_path_to_clinic_directory():
    """
    Returns the path to the clinic directory.
    """

    return os.path.join(os.environ["HOME"], 'code-clinic')


def get_path_to_config_file():
    """
    Returns the path to the config file in the user's home directory'
    """

    return os.path.join(os.environ["HOME"], 'code-clinic/config.json')


def update_config(email, location, days='7'):
    """
    Updates the config file in the user's home directory'
    """

    config_dict = {'username': email, 'campus': location, 'days': days}

    with open(get_path_to_config_file(), 'w') as file_object:
        json.dump(config_dict, file_object)


def check_if_config_file_exists():
    """
    Check if a config file exists at the given path
    """

    return os.path.exists(get_path_to_config_file())


def check_if_directory_exists():
    """
    Check if a directory exists at the given path
    """

    return os.path.exists(get_path_to_clinic_directory())


def create_empty_config_file():
    """
    Creates config file
    """

    if not check_if_directory_exists():
        create_config_directory()

    if not check_if_config_file_exists():
        with open(get_path_to_config_file(), 'w') as file_object:
            pass


def get_username():
    """
    Returns the username from the config file
    """

    with open(get_path_to_config_file(), 'r') as config:
        config_data = json.load(config)
        return config_data['username']


def get_campus_location() -> str:
    """
    Returns the campus location from the config file
    :return: The user's campus location
    """
    with open(get_path_to_config_file(), 'r') as config:
        config_data = json.load(config)
        return config_data['campus']


def get_days():
    """
    Returns the number of days from the config file
    :return: The number of days to be displayed in calendar
    """
    with open(get_path_to_config_file(), 'r') as config:
        config_data = json.load(config)
        return config_data['days']


def update_config_days(days):
    """
    Function enables the number of calendar days to be configurable. It updates the config file based on
    what the user has specified. 
    """
    config_data = {}
    with open(get_path_to_config_file(), 'r') as config:
        config_data = json.load(config)
    config_data['days'] = days
    update_config(config_data['username'],
                  config_data['campus'], config_data['days'])


def verify_config_file():
    """ 
    Verifies the configuration file
    """
    try:
        with open(get_path_to_config_file(), 'r') as config_file:
            config_data = json.load(config_file)
            return verify_config_data(config_data)

    except (FileNotFoundError, ValueError):
        return False


def verify_config_data(config_data):
    """
    Verifies the contents of the configuration file
    """
    try:
        return helpers.verify_email_address(config_data['username']) and \
               helpers.verify_campus_location(config_data['campus']) and \
               helpers.verify_config_days(config_data['days'])

    except KeyError:
        return False


def create_config_file():
    """ 
    Creates a local configuration file
    """

    code_clinic_output.welcome_msg()
    username = helpers.get_email_address()
    location = helpers.get_campus_location()
    create_empty_config_file()
    update_config(username, location)
    code_clinic_output.display_help()


def delete_config_file():
    """
    Deletes local configuration file
    """

    if check_if_config_file_exists():
        os.remove(get_path_to_config_file())
