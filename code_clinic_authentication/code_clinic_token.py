"""
Token module, handles everything relating to login tokens.

"""
from __future__ import annotations

import copy
import datetime
import os
import pickle

from google.auth import credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import code_clinic_api
import code_clinic_config
from code_clinic_io import code_clinic_output

SECRET_TOKEN: dict[str, dict[str | list[str]]] = {"installed": {
    "client_id": "364147813428-bkch7766kpe4ci474s9lni0ggb6gjqjg.apps.googleusercontent.com",
    "project_id": "testproject-339308",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

CLINIC_TOKEN = \
    {"token": "ya29.A0ARrdaM_Csd-9HxbnEE7f7gFg9PAiyouIu7Y8Lv86OtKZ3YN5EKTmS5GTbutpXjrQFIqb8cCAGZYAmBYhBKWBBhGpSTMh7liim7BA2CGqN1A-ZzB4eCKUlQ1_TN2BgnFEIPkyTl_cgFLJCVT1Sv54LgqLQt70",
     "refresh_token": "1//036bZqxhXOEWICgYIARAAGAMSNwF-L9Irl8WctElPwg5DLT3oR7W3Zea4_tERBbmsjz3rZ02A-75NRasw-KAd4a761U4FzhZoEcM",
     "token_uri": "https://oauth2.googleapis.com/token",
     "client_id": "364147813428-bkch7766kpe4ci474s9lni0ggb6gjqjg.apps.googleusercontent.com",
     "client_secret": "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",
     "scopes": ["https://www.googleapis.com/auth/calendar"],
     "expiry": "2022-02-15T17:27:07.108333Z"}

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_token_directory():
    """Creates a directory containing the token
    """
    os.makedirs(get_path_to_token_directory())


def get_path_to_token_directory():
    """Returns the path to the token directory"""

    return os.path.join(os.environ["HOME"], '.token/code_clinic')


def check_if_token_directory_exists():
    """Checks if the token directory exists and returns a boolean."""

    return os.path.exists(get_path_to_token_directory())


def get_path_to_user_token():
    """ Returns the path to the user directory """

    return os.path.join(get_path_to_token_directory(), 'user_token.pickle')


def check_if_user_token_exists():
    """Check if a user token exists"""

    return os.path.exists(get_path_to_user_token())


def create_user_token():
    """
    Creates the user token if it doesn't already exist'
    """
    if not check_if_token_directory_exists():
        create_token_directory()

    if not check_if_user_token_exists():
        with open(get_path_to_user_token(), 'wb') as token:
            pass


def connect() -> credentials.Credentials:
    """
    Connects to google calendar oauth and returns token credentials
    :return: Token credentials
    """
    flow = InstalledAppFlow.from_client_config(SECRET_TOKEN, SCOPES)

    return flow.run_local_server(port=0)


def return_user_token_creds():
    """
    Reads the user token from token pickle file
    """
    with open(get_path_to_user_token(), 'rb') as token_cred:
        return pickle.load(token_cred)


def return_clinic_credentials() -> credentials.Credentials:
    """
    Returns credential data from clinic token
    :return: Credential data
    """
    clinic_token_copy = copy.deepcopy(CLINIC_TOKEN)
    clinic_token_copy['expiry'] = \
        (datetime.datetime.now() + datetime.timedelta(hours= 1))\
        .isoformat() + '+02:00'
    return Credentials.from_authorized_user_info(clinic_token_copy,SCOPES)


def update_user_token(user_token_creds):
    """
    Updates the user token pickle file with the user token credentials
    """
    with open(get_path_to_user_token(), 'wb') as token:
        pickle.dump(user_token_creds, token)


def get_user_token(username):
    """Gets the user token by first checking if the token already exists"""

    if check_if_user_token_exists():
        user_token = return_user_token_creds()
        user_token.refresh(Request())

    else:
        create_user_token()
        code_clinic_output.output_login_prompt(username)
        user_token = connect()

    update_user_token(user_token)

    return user_token


def verify_user_token() -> bool:
    """
    Checks if the user token is valid or not
    :return: Boolean value
    """
    try:
        with open(get_path_to_user_token(), 'rb') as user_token:
            user_credentials = pickle.load(user_token)
            return user_credentials.valid
    except (EOFError, pickle.UnpicklingError, FileNotFoundError):
        return False


def check_user_token_expired() -> bool:
    """
    Checks if the user token has expired or not
    :return: Boolean value
    """
    if verify_user_token():
        return return_user_token_creds().expired
    return True


def delete_user_token() -> None:
    """
    Deletes the user token
    :return: None
    """
    if check_if_user_token_exists():
        os.remove(get_path_to_user_token())


def verify_user_credentials() -> None:
    """
    Deletes the user token if the username in the config file does not match
    the username from the token credentials
    :return: None
    """
    username: str = code_clinic_config.get_username()

    if not check_user_token_expired():
        user_token: credentials.Credentials = return_user_token_creds()

        if not code_clinic_api.verify_login(user_token, username):
            delete_user_token()
