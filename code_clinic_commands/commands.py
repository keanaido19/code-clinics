"""
Commands for the WTC Code Clinic Booking System.

"""
from google.auth import credentials

from code_clinic_io import code_clinic_output
import code_clinic_config
from code_clinic_authentication import code_clinic_token
import code_clinic_api
import datetime


def login():
    user_name = code_clinic_config.get_username()
    user_token = code_clinic_token.get_user_token(user_name)
    code_clinic_token.get_clinic_token()
    code_clinic_output.login_results()
    return user_token


def command_handler(command_arg):
    """It handles commands from the command line arguments.
    """
    if command_arg in {'-h', 'help', '--help'}:
        help_command()
        return
    elif command_arg == 'login':
        login()
        return
    elif code_clinic_token.check_user_token_expired():
        code_clinic_output.output_token_expired()
        return

    user_credentials: credentials.Credentials = \
        code_clinic_token.return_user_token_creds()

    clinic_credentials: credentials.Credentials = \
        code_clinic_token.return_clinic_credentials()

    if command_arg == 'student_calendar':
        display_calendar(user_credentials)
    elif command_arg == 'clinic_calendar':
        display_calendar(clinic_credentials)


def help_command():
    """
    Contains a list of valid commands.
    """
    code_clinic_output.display_help()


def display_calendar(token_creds):
    """
    Displays the google calendar results from the API
    """
    service = code_clinic_api.build_calendar_service(token_creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end = (datetime.datetime.utcnow() +
           datetime.timedelta(days=7)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=end,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time: str = \
            datetime.datetime.fromisoformat(start)\
                .strftime('%a %d-%b-%Y (%H:%M %p)')
        print(start_time, event['summary'])
