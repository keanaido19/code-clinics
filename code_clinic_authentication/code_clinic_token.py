"""
Token module, handles everything relating to login tokens.

"""
from __future__ import annotations
import os
import pickle
from code_clinic_io import code_clinic_output
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

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


def get_path_to_token():
    """ Returns the path to the user directory """

    return os.path.join(os.environ["HOME"], '.code-clinic/user_token.pickle')


def check_if_token_exists():
    """Check if a user token exists"""

    return os.path.exists(get_path_to_token())


def create_user_token():
    """
    Creates the user token if it doesn't already exist'
    """
    if not check_if_token_directory_exists():
        create_token_directory()

    if not check_if_token_exists():
        with open(get_path_to_token(), 'wb') as token:
            pass


def connect(connection_name, portnumber):
    """
    Establishes connection to google calendar api
    """

    flow = InstalledAppFlow.from_client_config(
        SECRET_TOKEN, ["https://www.googleapis.com/auth/calendar"])

    return flow.run_local_server(localhost=connection_name, port=portnumber)


def get_user_token_creds():
    """
    Reads the user token from token pickle file
    """
    with open(get_path_to_token(), 'rb') as token_cred:
        return pickle.load(token_cred)


def update_user_token(user_token_creds):
    """
    Updates the user token pickle file with the user token credentials
    """
    with open(get_path_to_token(), 'wb') as token:
        pickle.dump(user_token_creds, token)


def get_user_token(username):
    """Gets the user token by first checking if the token already exists"""

    if check_if_token_exists():
        user_token = get_user_token_creds()
        user_token.refresh(Request())

    else:
        create_user_token()
        code_clinic_output.login_prompt(username)
        user_token = connect('user_login', 8080)

    update_user_token(user_token)

    return user_token