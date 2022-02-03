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


def update_config(email):
    """
    Updates the config file in the user's home directory'
    """

    config_dict = {'username': email}

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