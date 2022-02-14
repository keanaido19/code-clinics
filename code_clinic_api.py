"""
Google calendar API calls.

"""
from __future__ import annotations

import itertools

from google.auth import credentials
from googleapiclient import discovery
from googleapiclient.discovery import build

import code_clinic_config
import helpers


def build_calendar_service(token_creds):
    """
    Builds the calendar service
    """

    return build('calendar', 'v3', credentials=token_creds)


def get_calendar_data(calendar_service):
    """
    get the calendar data for a given number of days
    """
    days = int(code_clinic_config.get_days())
    days = helpers.adjust_days_for_calendar_size(days)
    now, end = helpers.get_date_range(days)

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
    calendar_events = \
        helpers.remove_expired_calendar_events(calendar_data.get('items', []))
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
        clinic_credentials: credentials.Credentials,
        event_id: str, user_type: str) -> None:
    """
    Books the given WTC Code Clinic Booking System time slot
    :param credentials.Credentials clinic_credentials: Clinic token credentials
    :param str event_id: Calendar event id
    :param str user_type: str user_type: Type of user, volunteer or student
    :return: None
    """
    # Builds Google Calendar API service
    calendar_service: discovery.Resource = \
        build_calendar_service(clinic_credentials)

    # Retrieves calendar event from Google calendar using the event's id
    calendar_event: dict = \
        calendar_service.events()\
        .get(calendarId='primary', eventId=event_id).execute()

    # Retrieves the user's information from the config file
    username: str = code_clinic_config.get_username()
    campus_location: str = code_clinic_config.get_campus_location()

    # Set the events maximum allowable number of attendees
    calendar_event['maxAttendees']: int = 2

    # Sets the attendee data that will be added to the event
    attendee_data: dict[str, str] = \
        {
            'email': username,
            'comment': f'{user_type} - {campus_location}',
            'responseStatus': 'accepted',
        }

    # Checks for the events attendees and adds the user to the event's
    # attendees list
    if helpers.check_dictionary_key_is_valid('attendees', calendar_event):
        calendar_event['attendees'].append(attendee_data)
    else:
        calendar_event['attendees']: list[dict[str, str]] = [attendee_data]

    # Updates the Google Calendar event with the new modified event with the
    # user as an attendee
    calendar_service.events().update(
        calendarId='primary', eventId=event_id, body=calendar_event).execute()


def cancel_booking(
        clinic_credentials: credentials.Credentials, event_id: str) -> None:
    """
    Removes the user from the Google Calendar Event
    :param credentials.Credentials clinic_credentials: Clinic token credentials
    :param str event_id: Calendar event id
    :return: None
    """
    # Builds Google Calendar API service
    calendar_service: discovery.Resource = \
        build_calendar_service(clinic_credentials)

    # Retrieves calendar event from Google calendar using the event's id
    calendar_event: dict = \
        calendar_service.events() \
        .get(calendarId='primary', eventId=event_id).execute()

    # Retrieves the user's username from the config file
    username: str = code_clinic_config.get_username()

    # Removes the user from the 'attendees' key of the event dictionary
    for index, attendee in enumerate(calendar_event['attendees']):
        if attendee['email'] == username:
            calendar_event['attendees'].pop(index)

    # Updates the event on Google Calendar with the user removed from the
    # 'attendees' key of the event
    calendar_service.events().update(
        calendarId='primary', eventId=event_id, body=calendar_event).execute()
