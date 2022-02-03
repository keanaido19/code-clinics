"""
Commands for the WTC Code Clinic Booking System.

"""
from code_clinic_io import code_clinic_output
import code_clinic_config
from code_clinic_authentication import code_clinic_token
import code_clinic_api
import datetime


def login():
    user_name = code_clinic_config.get_username()
    token = code_clinic_token.get_user_token(user_name)
    code_clinic_output.login_results()
    return token


def command_handler(command_arg):
    """It handles commands from the command line arguments.
    """
    if command_arg == 'login':
        login()
    elif command_arg == 'student_calendar':
        pass
    elif command_arg == 'clinic_calendar':
        pass


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
        print(start, event['summary'])
