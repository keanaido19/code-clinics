"""
Google calendar API calls.

"""
from __future__ import annotations

from googleapiclient import discovery
from googleapiclient.discovery import build
import helpers
import itertools
from google.auth import credentials
import code_clinic_config



def build_calendar_service(token_creds):
    """
    Builds the calendar service
    """

    return build('calendar', 'v3', credentials=token_creds)


def get_calendar_data(calendar_service):
    """
    get the calendar data for a given number of days
    """

    now, end = helpers.get_date_range(7)

    return calendar_service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime').execute()


def get_calendar_events(calendar_data):
    '''
    This Function returns the events that a in a calendar
    '''
    calendar_events = calendar_data.get('items', [])
    for calendar_event in calendar_events:
        helpers.format_calendar_event(calendar_event)
    return calendar_events


def format_calendar_events(calendar_events):
    '''
    Formats the way that calendar events are returned to user.
    '''
    grouped_calendar_events = \
        itertools.groupby(
            calendar_events, key=lambda x: x['start']['event_date'])
    return {key: [value for value in values] for key, values in
            grouped_calendar_events}


def get_formatted_calendar_events(token_credentials):
    '''
    Retrieves the events and returns them in a formatted form.
    '''
    calendar_service = build_calendar_service(token_credentials)
    calendar_data = get_calendar_data(calendar_service)
    calendar_events = get_calendar_events(calendar_data)
    return format_calendar_events(calendar_events)


def book_code_clinic_time_slot(
        token_credentials: credentials.Credentials,
        event_id: str, user_type: str) -> None:
    """
    Books the given WTC Code Clinic Booking System time slot
    :param credentials.Credentials token_credentials: Token credentials
    :param str event_id: Calendar event id
    :param str user_type: str user_type: Type of user, volunteer or student
    :return: None
    """
    calendar_service: discovery.Resource = \
        build_calendar_service(token_credentials)

    calendar_event: dict = \
        calendar_service.events()\
        .get(calendarId='primary', eventId=event_id).execute()

    username: str = code_clinic_config.get_username()

    calendar_event['maxAttendees']: int = 2

    if helpers.check_dictionary_key_is_valid('attendees', calendar_event):
        calendar_event['attendees'].append(
            {
                'email': username,
                'comment': user_type,
                'responseStatus': 'accepted',
            }
        )
    else:
        calendar_event['attendees']: list[dict[str, str]] = \
            [{
                'email': username,
                'comment': user_type,
                'responseStatus': 'accepted',
            }]

    calendar_service.events().update(
        calendarId='primary', eventId=event_id, body=calendar_event).execute()
