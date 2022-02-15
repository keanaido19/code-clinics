"""
Token module, handles everything relating to login tokens.

"""
from __future__ import annotations

import os
import pickle
from typing import Optional

from google.auth import credentials
from google.auth.transport.requests import Request
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


def create_token_directory():
    """Creates a directory containing the token
    """
    os.makedirs(get_path_to_token_directory())


def get_path_to_token_directory():
    """Returns the path to the token directory"""

    return os.path.join(os.environ["HOME"], '.code-clinic')


def check_if_token_directory_exists():
    """Checks if the token directory exists and returns a boolean."""

    return os.path.exists(get_path_to_token_directory())


def get_path_to_user_token():
    """ Returns the path to the user directory """

    return os.path.join(os.environ["HOME"], '.code-clinic/user_token.pickle')


def get_path_to_clinic_token() -> str:
    """
    Returns the path to the code clinic's token
    :return: Path to the code clinic's token
    """
    return os.path.join(get_path_to_token_directory(), 'clinic_token.pickle')


def check_if_user_token_exists():
    """Check if a user token exists"""

    return os.path.exists(get_path_to_user_token())


def check_if_clinic_token_exists() -> bool:
    """
    Checks if the clinic token exists
    :return: Boolean value
    """
    return os.path.exists(get_path_to_clinic_token())


def create_user_token():
    """
    Creates the user token if it doesn't already exist'
    """
    if not check_if_token_directory_exists():
        create_token_directory()

    if not check_if_user_token_exists():
        with open(get_path_to_user_token(), 'wb') as token:
            pass


def create_clinic_token() -> None:
    """
    Creates an empty clinic token
    :return: None
    """
    if not check_if_clinic_token_exists():
        if not check_if_token_directory_exists():
            create_token_directory()
        with open(get_path_to_clinic_token(), 'wb'):
            ...


def connect() -> credentials.Credentials:
    """
    Connects to google calendar oauth and returns token credentials
    :return: Token credentials
    """
    flow = InstalledAppFlow.from_client_config(
        SECRET_TOKEN, ["https://www.googleapis.com/auth/calendar"]
    )

    return flow.run_local_server(port=0)


def return_user_token_creds():
    """
    Reads the user token from token pickle file
    """
    with open(get_path_to_user_token(), 'rb') as token_cred:
        return pickle.load(token_cred)


def return_clinic_credentials() -> credentials.Credentials:
    """
    Returns credential data from user token
    :return: Credential data
    """
    with open(get_path_to_clinic_token(), 'rb') as clinic_token:
        return pickle.load(clinic_token)


def update_user_token(user_token_creds):
    """
    Updates the user token pickle file with the user token credentials
    """
    with open(get_path_to_user_token(), 'wb') as token:
        pickle.dump(user_token_creds, token)


def update_clinic_token(token_credentials: Optional[credentials.Credentials])\
        -> None:
    """
    Updates the clinic token with login credential data
    :param credentials.Credentials token_credentials: Credential data
    :return: None
    """
    with open(get_path_to_clinic_token(), 'wb') as clinic_token:
        pickle.dump(token_credentials, clinic_token)


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


def get_clinic_token() -> credentials.Credentials:
    """
    Gets the clinic token data
    :return: Clinic token credentials
    """
    if check_if_clinic_token_exists():
        token_credentials = return_clinic_credentials()
        token_credentials.refresh(Request())
    else:
        create_clinic_token()
        code_clinic_output.output_login_prompt('team.a.obliviate@gmail.com')
        token_credentials = connect()
    update_clinic_token(token_credentials)
    return token_credentials


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


def verify_clinic_token() -> bool:
    """
    Checks if the clinic token is valid or not
    :return: Boolean value
    """
    try:
        with open(get_path_to_clinic_token(), 'rb') as clinic_token:
            clinic_credentials = pickle.load(clinic_token)
            return clinic_credentials.valid
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
