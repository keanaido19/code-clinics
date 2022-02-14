"""
Creates a config file.

"""
import os.path
import json


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


def update_config(email, location, days = '7'):
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


def create_config_file():
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
    update_config(config_data['username'], config_data['campus'], config_data['days'])