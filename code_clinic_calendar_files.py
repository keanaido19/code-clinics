"""
Local data files for WTC Code Clinic Booking System
"""

import os
import json


def get_path_to_calendar_file_directory():
    """
    Returns the path to the directory that will contain both user and clinic calendar data
    """

    return os.path.join(os.environ["HOME"], '.local/code_clinic/calendar_files')


def create_calendar_file_directory():
    """
    Creates the directory that will contain both user and clinic calendar data
    """

    return os.makedirs(get_path_to_calendar_file_directory())


def check_if_calendar_file_directory_exists():
    """
    Checks if the directory containing the calendar file exists
    """

    return os.path.exists(get_path_to_calendar_file_directory())


def get_path_to_user_calendar_file():
    """
    Returns the path to the user calendar file
    """

    return os.path.join(get_path_to_calendar_file_directory(), 'user_calendar.json')


def check_if_user_calendar_file_exists():
    """
    Checks if the user calendar file exists at the specified path
    """

    return os.path.exists(get_path_to_user_calendar_file())


def create_user_calendar_file():
    """
    Creates user calendar file if one doesn't already exist
    """

    if not check_if_user_calendar_file_exists():
        if not check_if_calendar_file_directory_exists():
            create_calendar_file_directory()

        with open(get_path_to_user_calendar_file(), 'w'):
            pass


def get_path_to_clinic_calendar_file():
    """
    Returns the path to the calendar data file
    """

    return os.path.join(get_path_to_calendar_file_directory(), 'clinic_calendar.json')


def check_if_clinic_calendar_file_exists():
    """
    Checks if the calendar calendar file exists at the specified path
    """

    return os.path.exists(get_path_to_clinic_calendar_file())


def create_clinic_calendar_file():
    """
    Creates clinic calendar file if one doesn't already exist
    """

    if not check_if_clinic_calendar_file_exists():
        if not check_if_calendar_file_directory_exists():
            create_calendar_file_directory()

        with open(get_path_to_clinic_calendar_file(), 'w'):
            pass


def read_user_calendar_file():
    """
    Read the user's calendar data file from the specified path'
    """

    try:
        with open(get_path_to_user_calendar_file(), 'r') as calendar_data:
            return json.load(calendar_data)

    except (FileNotFoundError, ValueError):
        return None


def read_clinic_calendar_file():
    """
    Reads the clinic data calendar file from the specified path
    """

    try:
        with open(get_path_to_clinic_calendar_file(), 'r') as calendar_data:
            return json.load(calendar_data)

    except (FileNotFoundError, ValueError):
        return None


def update_user_calendar_file(calendar_event_data):
    """
    Updates the user calendar data file
    """
    create_user_calendar_file()

    if calendar_event_data != read_user_calendar_file():
        with open(get_path_to_user_calendar_file(), 'w') as calendar_data:
            json.dump(calendar_event_data, calendar_data, indent=4)


def update_clinic_calendar_file(calendar_event_data):
    """
    Updates the clinic calendar data file
    """
    create_clinic_calendar_file()

    if calendar_event_data != read_clinic_calendar_file():
        with open(get_path_to_clinic_calendar_file(), 'w') as calendar_data:
            json.dump(calendar_event_data, calendar_data, indent=4)


def delete_user_calendar_file():
    '''It deletes the file for the user's calendar.
    '''
    if check_if_user_calendar_file_exists():
        os.remove(get_path_to_user_calendar_file())


def delete_clinic_calendar_file():
    '''It deletes the clinic's calendar file.
    '''
    if check_if_clinic_calendar_file_exists():
        os.remove(get_path_to_clinic_calendar_file())


def delete_calendar_files():
    '''It deletes all the calendar files.
    '''
    delete_user_calendar_file()
    delete_clinic_calendar_file()